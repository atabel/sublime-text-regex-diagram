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
        scope_reg = self.view.extract_scope(s.a) if s.a == s.b else s
        return self.view.substr(scope_reg)

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
