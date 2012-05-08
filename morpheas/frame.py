from .morph import *

class Frame(Morph):
    " I clip my submorphs at my bounds "

    def get_full_bounds(self):

        return self.bounds

    def get_wants_drop_of(self, morph):
        return True

    def full_draw_on(self, surface, rectangle=None):
        if rectangle == None:
            rectangle = self.full_bounds()
        rectangle = rectangle.intersect(self.full_bounds())
        self.draw_on(rectangle)
        for child in self.children:
            child.full_draw_on(surface, self.bounds.intersect(rectangle))

    def developers_menu(self):
        menu = super(Frame, self).developers_menu()
        menu.add_line()
        menu.add_item("move all inside...", 'keep_all_submorphs_within')
        return menu

    def keep_all_submorphs_within(self):
        for m in self.children:
            m.keep_within(self)
