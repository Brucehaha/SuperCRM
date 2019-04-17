from django.utils.safestring import mark_safe


class MyPaginator(object):
    def __init__(self, total_items, url="", num_per_page=20, max_num_pages=7, current_page = 1):
        self.total_items = total_items
        self.current_page = current_page
        self.url = url
        self.num_per_page = 20
        self.max_num_pages = max_num_pages

    def start(self):
        return (self.current_page-1)*self.total_items

    def end(self):
        return self.current_page*self.total_items

    def total_pages(self):
        a, b = divmod(self.total_items, self.num_per_page)
        if b:
            a += 1
        return a

    def page_range(self):
        first = last = 1

        if self.total_pages() < self.max_num_pages:
            return list(range(first, self.total_pages()))

        elif self.current_page <= self.max_num_pages//2:
            last = self.max_num_pages

        else:
            first = self.current_page-self.max_num_pages//2
            last = self.current_page + self.max_num_pages//2
            if first < 1:
                first = 1
            if last > self.total_pages():
                last = self.total_pages()
        return list(range(first, last))

    def paginator(self):
        _html = "<ul class='pagination'><li class='page-item'><a class='page-link' href ='%s?p=%s'>First Page</a></li>" %(
                    self.url,
                    1)
        is_active = ''
        if self.current_page != 1:
            _html += "<li class='page-item'><a class='page-link' href ='%s?p=%s'>Prev</a></li>" %(
                    self.url,
                    self.current_page - 1)
        else:
            _html += "<ul class='pagination'>" \
                     "<li class='page-item'><a class='page-link' href ='javascript:void(0)'>Previous</a></li>"

        for i in self.page_range():
            if self.current_page == i:
                is_active='active'

            _html += "<li class='page-item  %s'><a class='page-link' href='%s?p=%s'>%s</a></li>" % (
                    is_active,
                    self.url,
                    i, i)

        _html += "<li class='page-item'>" \
                 "<a class='page-link' href ='%s?p=%s'>Next</a></li></ul>" % (self.url, self.current_page + 1)

        _html += "<li class='page-item'><a class='page-link' href ='%s?p=%s'>Last Page</a></li></ul>" % (
            self.url, self.total_pages())

        _html += "%s Page of %s" % (
            self.current_page,  self.total_pages()
        )

        if self.max_num_pages <= 1:
            return ""
        return mark_safe(_html)










