from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.http import HttpResponse
from blog.models import Entry, Blogmark, Quotation


class Base(Feed):
    feed_type = Atom1Feed
    link = "/"
    author_name = "Jacob Kaplan-Moss"

    def __call__(self, request, *args, **kwargs):
        response = super(Base, self).__call__(request, *args, **kwargs)
        # Tell CloudFlare to cache my feeds for 2 minutes
        response['Cache-Control'] = 's-maxage=%d' % (2 * 60)
        return response

    def item_link(self, item):
        return item.get_absolute_url() + '#atom-%s' % self.ga_source

    def item_categories(self, item):
        return [t.tag for t in item.tags.all()]

    def item_pubdate(self, item):
        return item.created

    def item_updateddate(self, item):
        return item.created


class Entries(Base):
    title = "Jacob Kaplan-Moss: Writing"
    ga_source = 'entries'

    def items(self):
        return Entry.objects.prefetch_related(
            'tags'
        ).order_by('-created')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body


class Blogmarks(Base):
    title = "Jacob Kaplan-Moss: Blogmarks"
    description_template = "feeds/blogmark.html"
    ga_source = 'blogmarks'

    def items(self):
        return Blogmark.objects.prefetch_related(
            'tags'
        ).order_by('-created')[:15]

    def item_title(self, item):
        return item.link_title


class Everything(Base):
    title = "Jacob Kaplan-Moss"
    description_template = "feeds/everything.html"
    ga_source = 'everything'

    def items(self):
        # Pretty dumb implementation: pull top 30 of entries/blogmarks/quotations
        # then sort them together and return most recent 30 combined
        last_30_entries = list(Entry.objects.prefetch_related(
            'tags'
        ).order_by('-created')[:30])
        last_30_blogmarks = list(Blogmark.objects.prefetch_related(
            'tags'
        ).order_by('-created')[:30])
        last_30_quotations = list(Quotation.objects.prefetch_related(
            'tags'
        ).order_by('-created')[:30])
        combined = last_30_blogmarks + last_30_entries + last_30_quotations
        combined.sort(key=lambda e: e.created, reverse=True)
        return combined[:30]

    def item_title(self, item):
        if isinstance(item, Entry):
            return item.title
        elif isinstance(item, Blogmark):
            return item.link_title
        else:
            return 'Quoting %s' % item.source


def sitemap(request):
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for klass in (Entry, Blogmark, Quotation):
        for obj in klass.objects.only('slug', 'created'):
            url = request.build_absolute_uri(obj.get_absolute_url)
            xml.append(f'<url><loc>{url}</loc></url>')
    xml.append('</urlset>')
    return HttpResponse('\n'.join(xml), content_type='application/xml')
