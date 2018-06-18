import json
import logging
import requests

from django.conf import settings


def create_experiment_bug(experiment):
    bug_data = {
        "product": "Shield",
        "component": "Shield Study",
        "version": "unspecified",
        "summary": "[Shield] Pref Flip Study: {name}".format(
            name=experiment.name
        ),
        "description": experiment.BUGZILLA_TEMPLATE.format(
            experiment=experiment
        ),
        "assigned_to": experiment.owner.email,
        "cc": settings.BUGZILLA_CC_LIST,
    }

    try:
        response = requests.post(settings.BUGZILLA_CREATE_URL, bug_data)
        response_data = json.loads(response.content)

        experiment.bugzilla_id = response_data["id"]
        experiment.save()
    except requests.exceptions.RequestException:
        logging.exception("Error creating Bugzilla Ticket")
