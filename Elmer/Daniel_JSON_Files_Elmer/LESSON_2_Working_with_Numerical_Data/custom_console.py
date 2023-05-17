from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from PyQt6.QtCore import pyqtSignal


class CustomPythonConsole(RichJupyterWidget):
    code_executed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()
        self.setMinimumHeight(200)
        self.kernel_client.iopub_channel.message_received.connect(self.handle_message_received)

    def handle_message_received(self, msg):
        msg_type = msg['header']['msg_type']
        if msg_type == 'execute_result':
            if 'content' in msg and 'data' in msg['content']:
                output = msg['content']['data'].get('text/plain', '')
                self.code_executed.emit(output)
