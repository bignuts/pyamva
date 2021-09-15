import npyscreen
from database import IDatabase, Param
from util import list_to_str, str_to_list, str_to_bool, TimeIt
from getter import IGetter
from adapter import IAdapter
from converter import IConverter
from marketscreen import MarketScreen
from typing import List, Iterable, Optional
import curses
from plot import PlotComposite


class MyGrid(npyscreen.GridColTitles):

    def __init__(self, *args, **keywords):
        super(MyGrid, self).__init__(*args, **keywords)
        self.add_handlers({curses.ascii.SP: self.do_stuff})

    # overwrite method
    def do_stuff(self, *args, **keywords):
        pass


class ParameterListForm(npyscreen.ActionFormMinimal):

    OK_BUTTON_TEXT = 'Exit'

    def create(self):
        self.name = 'Parameter Screen'
        self.__addbtn = self.add(AddSymbolButtonWidget)
        self.__calcbtn = self.add(CalculateButtonWidget)
        titles = ['Symbol', 'Timeframe', 'Lookback', 'Decimals',
                  'Offset', 'Tpo size', 'Profiles', 'Active']
        self.__prm = self.add(ParamGrid,
                              col_titles=titles,
                              columns=len(titles),
                              default_column_number=len(titles),
                              select_whole_line=True)

    def beforeEditing(self):
        self.__update_list()

    def __update_list(self):
        lst = self.parentApp._db.get_all()
        lst = [param.to_list() for param in lst]
        self.__prm.values = lst
        # TODO aggiungi support per il colore qua, chiama metodo dalla classe
        self.__prm.display()

    def on_ok(self):
        self.parentApp.getForm('EXIT').set_ok_form(None)
        self.parentApp.setNextForm('EXIT')


class AddSymbolButtonWidget(npyscreen.ButtonPress):

    def __init__(self, *args, **keywords):
        super(AddSymbolButtonWidget, self).__init__(*args, **keywords)
        self.name = 'Add symbol'
        self.relx = 1
        self.rely = 3

    def whenPressed(self):
        self.parent.parentApp.switchForm('ADDFORM')


class CalculateButtonWidget(npyscreen.ButtonPress):

    def __init__(self, *args, **keywords):
        super(CalculateButtonWidget, self).__init__(*args, **keywords)
        self.name = 'Calculate'
        self.relx = 12
        self.rely = 3

    def whenPressed(self):
        with TimeIt('Find balance'):
            self.parent.parentApp._mrkt.first_day_balance(
                db=self.parent.parentApp._db)
        self.parent.parentApp.switchForm('MARKET')


class ParamGrid(MyGrid):

    def __init__(self, *args, **keywords):
        super(ParamGrid, self).__init__(*args, **keywords)
        self.rely = 5

    def do_stuff(self, *args, **keywords):
        row = self.edit_cell[0]
        symbol = self.values[row][0]
        self.parent.parentApp.getForm('EDITFORM').value = symbol
        self.parent.parentApp.switchForm('EDITFORM')

    def custom_print_cell(self, actual_cell, cell_display_value):
        if cell_display_value == 'False':
            actual_cell.color = 'DANGER'
        elif cell_display_value == 'True':
            actual_cell.color = 'GOOD'
        else:
            actual_cell.color = 'DEFAULT'


class ExitPopUpForm(npyscreen.ActionPopup):

    def __init__(self, *args, **keywords):
        super(ExitPopUpForm, self).__init__(*args, **keywords)
        self.name = 'Exit form'
        self.__ok_form: Optional[str] = None

    def create(self):
        self.add(npyscreen.FixedText,
                 value='Are you sure you want to quit?')

    def on_ok(self):
        self.parentApp.setNextForm(self.__ok_form)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def set_ok_form(self, ok_form: Optional[str]):
        self.__ok_form = ok_form


class AddRecordForm(npyscreen.ActionForm):

    OK_BUTTON_TEXT = 'Add'
    CANCEL_BUTTON_TEXT = 'Cancel'

    def create(self):
        self.__symbol = self.add(npyscreen.TitleText, name='Symbol:')
        self.__timeframe = self.add(npyscreen.TitleText, name='Timeframe:')
        self.__days = self.add(npyscreen.TitleText, name='Lookback:')
        self.__decimal = self.add(npyscreen.TitleText, name='Decimals:')
        self.__offset = self.add(npyscreen.TitleText, name='Offset:')
        self.__tpo_size = self.add(npyscreen.TitleText, name='Tpo size:')
        self.__profiles = self.add(npyscreen.TitleText, name='Profiles:')
        self.__active = self.add(npyscreen.TitleText, name='Active:')

    def beforeEditing(self):
        self.name = 'New Symbol'
        self.__symbol.value = ''
        self.__timeframe.value = ''
        self.__days.value = ''
        self.__decimal.value = ''
        self.__offset.value = ''
        self.__tpo_size.value = ''
        self.__profiles.value = ''
        self.__active.value = ''

    def on_ok(self):
        p = Param(symbol=self.__symbol.value,
                  timeframe=self.__timeframe.value,
                  days=int(self.__days.value),
                  decimal=int(self.__decimal.value),
                  offset=int(self.__offset.value),
                  tpo_size=int(self.__tpo_size.value),
                  profiles=str_to_list(self.__profiles.value),
                  active=str_to_bool(self.__active.value))
        self.parentApp._db.add(p)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class EditRecordForm(npyscreen.ActionForm):

    OK_BUTTON_TEXT = 'Update'
    CANCEL_BUTTON_TEXT = 'Delete'
    CANCEL_BUTTON_BR__offset = (2, 16)

    def create(self):
        self.__symbol = self.add(npyscreen.TitleFixedText, name='Symbol:')
        self.__timeframe = self.add(npyscreen.TitleText, name='Timeframe:')
        self.__days = self.add(npyscreen.TitleText, name='Lookback:')
        self.__decimal = self.add(npyscreen.TitleText, name='Decimals:')
        self.__offset = self.add(npyscreen.TitleText, name='Offset:')
        self.__tpo_size = self.add(npyscreen.TitleText, name='Tpo size:')
        self.__profiles = self.add(npyscreen.TitleText, name='Profiles:')
        self.__active = self.add(npyscreen.TitleText, name='Active:')

    def beforeEditing(self):
        param = self.parentApp._db.get(self.value)
        self.name = f"Edit {param.symbol}"
        self.__symbol.value = param.symbol
        self.__timeframe.value = param.timeframe
        self.__days.value = str(param.days)
        self.__decimal.value = str(param.decimal)
        self.__offset.value = str(param.offset)
        self.__tpo_size.value = str(param.tpo_size)
        self.__profiles.value = list_to_str(param.profiles)
        self.__active.value = str(param.active)

    def on_ok(self):
        p = Param(symbol=self.__symbol.value,
                  timeframe=self.__timeframe.value,
                  days=int(self.__days.value),
                  decimal=int(self.__decimal.value),
                  offset=int(self.__offset.value),
                  tpo_size=int(self.__tpo_size.value),
                  profiles=str_to_list(self.__profiles.value),
                  active=str_to_bool(self.__active.value))
        self.parentApp._db.update(p)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp._db.remove(self.value)
        self.parentApp.switchFormPrevious()


class MarketscreenForm(npyscreen.ActionFormMinimal):

    OK_BUTTON_TEXT = 'Exit'

    def create(self):
        self.name = 'Market Screen'
        self.__bal = self.add(MarketscreenWidget)

    def beforeEditing(self):
        self.__update_list()

    def __update_list(self):
        l = self.parentApp._mrkt.get_balanced_days_only(1, True)
        t = tuple(l)
        self.__bal.values = t
        self.__bal.display()

    def on_ok(self):
        self.parentApp.getForm('EXIT').set_ok_form('MAIN')
        self.parentApp.switchForm('EXIT')


class MarketscreenWidget(npyscreen.MultiLineAction):

    def display_value(self, vl):
        return f'{vl}'

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp._mrkt.all_day_balance(
            self.parent.parentApp._db.get(act_on_this))
        # calcola vty
        self.parent.parentApp._mrkt.find_reference_1(
            self.parent.parentApp._db.get(act_on_this)
        )

        self.parent.parentApp._mrkt.find_reference_2(
            self.parent.parentApp._db.get(act_on_this)
        )

        self.parent.parentApp.getForm(
            'BALANCE').name = act_on_this
        self.parent.parentApp.switchForm('BALANCE')


class BalanceGrid(MyGrid):

    def __init__(self, *args, **keywords):
        super(BalanceGrid, self).__init__(*args, **keywords)

    def do_stuff(self, *args, **keywords):
        row = self.edit_cell[0]
        date = self.values[row][0]
        symbol = self.parent.name
        ref_list = self.parent.parentApp._mrkt[symbol][date]
        # grafico qua
        plot = PlotComposite()
        # plot.plot_single(ref_list[2])
        plot.plot_multiple(ref_list)
        # self.parent.parentApp.getForm('EDITFORM').value = symbol
        # self.parent.parentApp.switchForm('EDITFORM')

    def custom_print_cell(self, actual_cell, cell_display_value):
        if cell_display_value == 'L Alert' or cell_display_value == 'S Alert':
            actual_cell.color = 'GOOD'
        elif cell_display_value == 'Bracket L' or cell_display_value == 'Bracket S':
            actual_cell.color = 'DEFAULT'
        elif cell_display_value == 'Trending':
            actual_cell.color = 'DANGER'
        else:
            actual_cell.color = 'DEFAULT'


class BalanceListForm(npyscreen.ActionFormMinimal):

    OK_BUTTON_TEXT = 'Exit'

    def create(self):
        self.__bal = self.add(BalanceGrid, select_whole_line=True)

    def beforeEditing(self):
        self.__update_list()

    def __update_list(self):
        rep = self.parentApp._mrkt[self.name]
        titles = ['End Time', 'VTY'] + rep.get_titles()
        lst = rep.bracket_list()
        self.__bal.col_titles = titles
        self.__bal.columns = len(titles)
        self.__bal.default_column_number = len(titles)
        self.__bal.values = lst
        self.__bal.display()

    def on_ok(self):
        self.parentApp.getForm('EXIT').set_ok_form('MARKET')
        self.parentApp.switchForm('EXIT')


class AmvaApplication(npyscreen.NPSAppManaged):

    def __init__(self, db: IDatabase, g: IGetter, a: IAdapter, c: IConverter):
        super().__init__()
        self._db = db
        self._mrkt = MarketScreen(g, a, c)

    def onStart(self):
        self.addForm('MAIN', ParameterListForm)
        self.addForm('EXIT', ExitPopUpForm)
        self.addForm('ADDFORM', AddRecordForm)
        self.addForm('EDITFORM', EditRecordForm)
        self.addForm('MARKET', MarketscreenForm)
        self.addForm('BALANCE', BalanceListForm)
