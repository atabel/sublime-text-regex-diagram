import sublime
import sublime_plugin
import webbrowser
import urllib


class ViewRegExpDiagramCommand(sublime_plugin.TextCommand):
    SERVICE_URL = "http://www.regexper.com/#"

    def run(self, edit=None, regexp=None):
        if regexp is None:
            regexp = self.selection()

        regexp = self.strip_quotes(regexp)
        webbrowser.open_new_tab(self.build_url(regexp))

    def selection(self):
        s = self.view.sel()[0]

        start = s.a
        end = s.b

        # if nothing is selected, expand selection to nearest terminators
        if start == end:
            view_size = self.view.size()
            terminator = '/\"\''

            # move the selection back to the start of the RegExp
            while (start > 0
                    and not self.view.substr(start - 1) in terminator
                    and self.view.classify(start) & sublime.CLASS_LINE_START == 0):
                start -= 1

            # move end of selection forward to the end of the RegExp
            while (end < view_size
                    and not self.view.substr(end) in terminator
                    and self.view.classify(end) & sublime.CLASS_LINE_END == 0):
                end += 1

        return self.view.substr(sublime.Region(start, end)).strip()

    def strip_quotes(self, regexp):
        if (
            (regexp.startswith("\"") and regexp.endswith("\""))
            or (regexp.startswith("\'") and regexp.endswith("\'"))
            or (regexp.startswith("/") and regexp.endswith("/"))
        ):
            regexp = regexp[1:-1]

        return regexp

    def build_url(self, regexp):
        url_encoded_regexp = urllib.parse.quote(regexp)
        return self.SERVICE_URL + url_encoded_regexp
