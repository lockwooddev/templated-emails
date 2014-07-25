from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template

from .utils import get_email_directories
from .parse_util import recursive_block_replace

import logging


logger = logging.getLogger('templated_emails')


def index(request, template_name="templated_emails/index.html"):
    if not request.user.is_superuser:
        raise Http404
    else:
        directory_tree = get_email_directories(settings.EMAIL_TEMPLATES_DIRECTORY)
        return render_to_response(
            template_name,
            {"directory_tree": directory_tree},
            context_instance=RequestContext(request))


def view(request, path, template_name="templated_emails/view.html"):
    if not request.user.is_superuser:
        raise Http404
    else:
        # get extends node
        # get all block nodes
        # do this recursive until no more extends
        # then place html in blocks
        rendered_subject = ""
        rendered_html = ""
        rendered_text = ""

        # make sure the path is relative
        path = path.lstrip('/')

        try:
            template = get_template("{}/email.html".format(path))
            rendered_html = recursive_block_replace(template, {})
        except:
            logger.exception("Error rendering templated email email.html")

        try:
            template = get_template("{}/email.txt".format(path))
            rendered_text = recursive_block_replace(template, {})
        except:
            logger.exception("Error rendering templated email email.txt")

        try:
            template = get_template("{}/short.txt".format(path))
            rendered_subject = recursive_block_replace(template, {})
        except:
            logger.exception("Error rendering templated email short.txt")

        return render_to_response(
            template_name,
            {
                "rendered_subject": rendered_subject,
                "rendered_html": rendered_html,
                "rendered_text": rendered_text,
            },
            context_instance=RequestContext(request))
