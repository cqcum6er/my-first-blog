#Collect a bunch of url's as a shortcut list (usage: collect 'html' as 'shortcut').
from django import template

register = template.Library()

@register.tag
def collect(parser, token):
    bits = list(token.split_contents())
    if len(bits) > 3 and bits[-2] == 'as':  #Define syntax for positional argument.
        varname = bits[-1]  #Last positonal argument is reserved for shortcut list name.
        items = bits[1:-2]  #Every url between 'collect' and 'as' is collected.
        return CollectNode(items, varname)
    else:
        raise template.TemplateSyntaxError('%r expected format is "item [item ...] as varname"' % bits[0])

class CollectNode(template.Node):
    def __init__(self, items, varname):
        self.items = map(template.Variable, items)
        self.varname = varname

    def render(self, context):
        context[self.varname] = [i.resolve(context) for i in self.items]
        return ''