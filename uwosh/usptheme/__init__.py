from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from webcouturier.dropdownmenu.browser.dropdown import DropdownMenuViewlet as BaseDropdownMenuViewlet
from plone.app.layout.viewlets.common import SearchBoxViewlet as BaseSearchBoxViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DropdownMenuViewlet(BaseDropdownMenuViewlet):
    _template = ViewPageTemplateFile('dropdown_sections.pt')

    def update(self):
        super(DropdownMenuViewlet, self).update()
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        props = getToolByName(self.context, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            self.search_input_id = "searchGadget"
        else:
            self.search_input_id = "nolivesearchGadget" # don't use "" here!

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())

        # normal GlobalSectionsViewlet stuff
        context = aq_inner(self.context)
        portal_tabs_view = getMultiAdapter((context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']


class SearchBoxViewlet(BaseSearchBoxViewlet):
    index = ViewPageTemplateFile('searchbox.pt')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
