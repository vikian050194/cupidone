import abc

from cupidone.views import *
from cupidone.printers import *
from cupidone.configuration import Configuration, OutputFlagValues


class AbstractOutputManager(abc.ABC):
    @abc.abstractmethod
    def emmit(self,  view: AbstractView):
        raise NotImplementedError()


class OutputManager(AbstractOutputManager):
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.printer: BasePrinter = None

        if configuration.output == OutputFlagValues.HUMAN:
            self.printer = HumanPrinter()
        if configuration.output == OutputFlagValues.PLAIN:
            self.printer = PlainPrinter()
        if configuration.output == OutputFlagValues.JSON:
            self.printer = JsonPrinter()

    def _print_str(self, message):
        self.printer.print_str(message)

    def _print_message(self, message: MessageView):
        self.printer.print_message(message)

    def _print_list(self, list):
        self.printer.print_list(list)

    def _print_object(self, object):
        self.printer.print_object(object)


    def emmit(self,  view: AbstractView):
        if type(view) is StrView:
            self._print_str(view)
        elif type(view) is InfoView:
            self._print_message(view)
        elif type(view) is WarningView:
            self._print_message(view)
        elif type(view) is ErrorView:
            self._print_message(view)
        elif type(view) is ListView:
            self._print_list(view.list)
        else:
            self._print_str("unknown view")


__all__ = ["OutputManager"]
