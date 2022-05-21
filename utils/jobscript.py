from database.env import *
import os

class Jobscript(object):

    def __init__(self):
        self.job_env = {}

    def submit_to_farm(self):
        self.job_env = {'engine': '123.456.789.10',
                        'service': 'nukeuser',
                        'priority': 95,
                        'name': os.environ.get('HOSTNAME'),
                        'tool': 'Eleve',
                        'ffmpeg': self.ffmpeg,
                        'input': self.input,
                        'output': self.output,
                        'output_mov': self.output_mov,
                        'start_frame': self.start_frame,
                        'current_category': self.output.split('/')[-2],
                        'top_level_category': self.output.split('/')[-3],
                        'group': self.output.split('/')[-4],
                        'gizmos': config['gizmos']
                        }
        basename = os.path.basename(self.job_env.get('output'))
        if '@' in basename:
            self.job_env['title'] = os.path.splitext(basename.split('@')[-1])[0]
        else:
            self.job_env['title'] = os.path.splitext(basename)[0]
        self.job_env['MAIN_TITLE'] = "[{tool}] {current_category} / {title} ({group})".format(**self.job_env)

        tmp_path = '{0}/{1}'.format(config['alftmp'], self.job_env.get('group'))

        file_alf = self.make_alf(tmp_path, self.job_env)
        self.execute_spool(file_alf)

    def execute_spool(self, alf):
        """send to farm by spool api
        Args:alf(str): path of alf file
        Returns:
        """
        cmd = '{0} --engine="{1}" --user="{2}" --projects="{3}" ' \
              '--priority="{4}" {5}' \
            .format(config['spool'], self.job_env.get('engine'),
                    self.job_env.get('name'), self.job_env.get('tool'),
                    self.job_env.get('priority'), alf)
        print(cmd)
        os.popen(cmd).read()

    def make_alf(self, tmp_path, env):
        """make alf file
        Args:
            tmp_path(str): path of nuke script file
            env(dict): environment variables
            node(list): list of node's dictionary
        Returns(str): alf file path
        """

        # save alf file
        code = "Job -title {{{MAIN_TITLE}}} \\\n" \
               "    -service {{{service}}} \\\n" \
               "    -serialsubtasks 1 \\\n" \
               "    -tags {{eleve}} \\\n" \
               "    -atleast 1 -atmost 12 -samehost 8 \\\n" \
               "    -init {{}} \\\n" \
               "    -envkey {{{{nuke-9.0v8}} {{setenv \\\n" \
               "     NUKE_PATH={gizmos} \\\n" \
               "     NAME={name} \\\n".format(**env)
        code += "     }} \\\n"

        # master task
        code += "-subtasks {{\n" \
                "Task -title {{[{tool}] {title} ({group})}} " \
                "-serialsubtasks 0 -subtasks {{\n".format(**env)
        code += "    Task -title {{ (Thumbnail) {0} }} " \
                "-subtasks {{\n".format(self.job_env['title']+'.gif')
        code += "    Task -title {{ (Preview_mov) {0} }} " \
                "-subtasks {{\n".format(self.job_env['title']+'.mov')

        if self.job_env['group'] == "Comp_Source":
            code += "    } \\\n"
            code += "    -cmds {{RemoteCmd {{{0}}} \n" \
                    "    }}\n".format(' '.join(self.convert_mov()))
            code += "    } \\\n"
            code += "    -cmds {{RemoteCmd {{{0}}} \n" \
                    "    }}\n".format(' '.join(self.convert_thumb()))

            code += "}} -cmds {{RemoteCmd {{{0}" \
                    "}}\n".format(' '.join(self.final_check_state()))

        elif self.job_env['group'] == "Reference":
            code += "    } \\\n"
            code += "    -cmds {{RemoteCmd {{{0}}} \n" \
                    "    }}\n".format(' '.join(self.convert_ref_mov()))
            code += "    } \\\n"
            code += "    -cmds {{RemoteCmd {{{0}}} \n" \
                    "    }}\n".format(' '.join(self.convert_ref_thumb()))

            code += "}} -cmds {{RemoteCmd {{{0}" \
                    "}}\n".format(' '.join(self.final_ref_check_state()))

        code += '}}'

        # make temp nk file
        tmp_alf_name = '{0}.alf'.format(self.job_env.get('title'))
        alf_path = os.path.join(tmp_path, tmp_alf_name)

        alf_file = file(alf_path, 'w')
        alf_file.write(code)
        alf_file.close()

        return alf_path

    def convert_mov(self):
        cmds = ['{}/Eleve_Slate'.format(config['gizmos']),
                self.job_env.get('input'),
                self.output_mov]

        return cmds

    def convert_thumb(self):
        if not os.path.isfile(self.output):
            cmds = [self.job_env.get('ffmpeg'),
                    "-y",
                    "-i",
                    self.output_mov,
                    "-vf",
                    "scale={}:{}:force_original_aspect_ratio=decrease".format(
                        config['DIMENSION_X'], config['DIMENSION_Y']
                    ),
                    "-r",
                    "24",
                    self.output,
                    "-hide_banner"]

            return cmds

    def convert_ref_mov(self):
        if not os.path.isfile(self.output):
            cmds = [self.job_env.get('ffmpeg'),
                    "-y",
                    "-i",
                    '"{}"'.format(self.job_env.get('input')),
                    "-vcodec libx264",
                    "-pix_fmt yuv420p",
                    "-g 30",
                    "-b:v 1500k",
                    "-vprofile high",
                    "-bf 0",
                    "-f mp4",
                    '-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"',
                    self.output_mov]

            return cmds

    def convert_ref_thumb(self):
        if not os.path.isfile(self.output):
            cmds = ["{}/Ref_preview.sh".format(config['gizmos']),
                    '"{}"'.format(self.output_mov),
                    '"{}"'.format(self.output)]

            return cmds

    def final_check_state(self):
        fin_data = {'item': self.item, 'current_category': self.job_env.get('current_category'),
                    'top_level_category': self.job_env.get('top_level_category'),
                    'group': self.job_env.get('group'), 'output': self.output}
        cmds = ["/core/Linux/APPZ/Python/2.7/bin/python",
                "{}/utils/convert_finished.py".format(Eleve_root),
                '"{}"'.format(fin_data)]

        return cmds

    def final_ref_check_state(self):
        fin_data = {'item': self.output_mov, 'current_category': self.job_env.get('current_category'),
                    'top_level_category': self.job_env.get('top_level_category'),
                    'group': self.job_env.get('group'), 'output': self.output}
        cmds = ["/core/Linux/APPZ/Python/2.7/bin/python",
                "{}/utils/convert_finished.py".format(Eleve_root),
                '"{}"'.format(fin_data)]

        return cmds
