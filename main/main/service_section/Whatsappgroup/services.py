from service_section.Whatsappgroup.models import WhatsappGroup

def get_whatsapp_links (Serviceorder):
    groups = WhatsappGroup.objects.filter (
        product__in = Serviceorder.products.all(),
        student_class = Serviceorder.student_class,
        is_active = True
    )

    links = []
    for group in groups:
        links.append(group.group_link)
    return links