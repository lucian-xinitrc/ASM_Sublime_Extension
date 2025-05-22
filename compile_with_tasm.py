import sublime
import sublime_plugin
import os
import shutil
import subprocess
import time

class CompileWithTasmCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_path = self.view.file_name()

        if not file_path:
            sublime.message_dialog("Save the file before compiling.")
            return

        if not file_path.endswith(".asm"):
            sublime.message_dialog("Only .asm files are supported.")
            return

        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        exec_path = os.path.join(file_dir, "tasm_dir", "EXEC.ASM")
        output_txt = os.path.join(file_dir, "tasm_dir", "OUTPUT.TXT")
        output_lst = os.path.join(file_dir, "tasm_dir", "EXEC.LST")

        try:
            shutil.copy(file_path, exec_path)

            dosbox_command = (
                'dosbox -c "mount C ." '
                '-c "C:" '
                '-c "cd tasm_dir" '
                '-c "TASM /zi /l EXEC.ASM" '
                '-c "TLINK /v /3 EXEC.OBJ" '
                '-c "EXEC.EXE" '
                '-c "DEL EXEC.ASM" '
                '-c "DEL EXEC.OBJ" '
                '-c "DEL EXEC.EXE" '
                #'-c "exit"'
            )

            subprocess.Popen(["terminator", "-e", dosbox_command], cwd=file_dir)

            sublime.set_timeout_async(lambda: self.load_output(output_txt), 5000)
            sublime.set_timeout_async(lambda: self.load_output(output_lst), 5000)

        except Exception as e:
            sublime.message_dialog("Error: " + str(e))

    def load_output(self, output_txt):
        if os.path.exists(output_txt):
            with open(output_txt, "r") as f:
                content = f.read()
                self.show_output(content)
        else:
            sublime.message_dialog("Compilation may have failed or OUTPUT.TXT not created.")

    def show_output(self, content):
        output_view = self.view.window().new_file()
        output_view.set_name("TASM Output")
        output_view.set_scratch(True)
        output_view.run_command("append", {"characters": content})
