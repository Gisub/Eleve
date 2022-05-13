import nuke
from main import *
from nukescripts import panels


nuke.menu('Nuke').addCommand('M83/Eleve', 'main()', 'F9')


class ElevePanel(nukescripts.PythonPanel):
    def __init__(self):
        super(ElevePanel, self).__init__(title="Eleve", id="uk.co.thefoundry.ElevePanel")
        self.pyKnob = nuke.PyCustom_Knob("", "", "EleveKnob()")
        self.addKnob(self.pyKnob)


class EleveKnob:

    def makeUI(self):
        self.eleve = Eleve()
        return self.eleve


eleve_wid = ElevePanel()
nuke.menu('Pane').addCommand("Eleve", "eleve_wid.addToPane()")
