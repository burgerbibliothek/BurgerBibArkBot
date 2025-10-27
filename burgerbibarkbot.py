import re
import requests
import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import ExistingPageBot


class BurgerBibArkBot(ExistingPageBot):

    update_options = {
        'summary': 'BurgerBibArkBot: Added persistent links.',
    }

    def getARK(self, id):
        """ Retrieve assigned name part of ARK from detailpage in catalogue """
        r = requests.get(f"https://katalog.burgerbib.ch/detail.aspx?ID={id}")
        regex_ark = r"(?<=ark:36599\/).+(?=\" )"
        ark = re.findall(regex_ark, r.text)
        return ark

    def treat_page(self):
        """Search and replace BurgerBib Templates without persistent links"""
        text = self.current_page.text
        regex_template = r"{{BurgerBib\|.+}}"
        matches = re.findall(regex_template, text, re.MULTILINE)

        for match in matches:
            to_replace = match
            match = match[2:-2]
            match = match.split("|")

            if len(match) > 1 and match[1].isnumeric():
                ark = self.getARK(id=match[1])

                if ark:
                    if len(match) == 4 and not match[3]:
                        match[3] = ark[0]
                    elif len(match) == 3:
                        match.append(ark[0])
                    elif len(match) == 2:
                        match.append('')
                        match.append(ark[0])

            match = '|'.join(match)
            replacement = "{{"+match+"}}"
            text = text.replace(to_replace, replacement)

        """Search for non-persistent and obsolete links and replace them"""
        regex_template = r"https?\:\/{2}(?:burgerbib\.scopeoais|katalog\.burgerbib)\.ch\/detail\.aspx\?ID\=[0-9]*"
        matches = re.findall(regex_template, text, re.MULTILINE | re.IGNORECASE)

        for match in matches:
            to_replace = match
            match = match.split("=")

            if len(match) > 1 and match[1].isnumeric():
                ark = self.getARK(id=match[1])

                if ark:
                    text = text.replace(to_replace, f"https://ark.burgerbib.ch/ark:36599/{ark[0]}")

        
        self.put_current(text, summary=self.opt.summary)

def main():
    """Parse command line arguments and invoke bot."""
    options = {}
    gen_factory = pagegenerators.GeneratorFactory()

    # Option parsing
    local_args = pywikibot.handle_args()  # global options
    local_args = gen_factory.handle_args(local_args)  # generators options
    for arg in local_args:
        opt, sep, value = arg.partition(':')
        if opt in ('-summary', '-text'):
            options[opt[1:]] = value

    BurgerBibArkBot(generator=gen_factory.getCombinedGenerator(), **options).run()

if __name__ == '__main__':
    main()

