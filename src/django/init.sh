#!/bin/bash
#set -o errexit
#set -o pipefail
#set -o nounset
# . ./.env
python manage.py makemigrations
python manage.py migrate


python manage.py resetdb


python manage.py waffle_switch vector_tile on
python manage.py waffle_switch claim_a_facility on
python manage.py waffle_switch ppe on
python manage.py waffle_switch report_a_facility on
python manage.py waffle_switch embedded_map on
python manage.py waffle_switch extended_profile on


python manage.py processfixtures


python manage.py user_groups -e c2@example.com -a add -g can_submit_facility
python manage.py user_groups -e c2@example.com -a add -g can_submit_private_facility
python manage.py user_groups -e c2@example.com -a add -g can_get_facility_history
python manage.py user_groups -e c2@example.com -a add -g can_view_full_contrib_detail

python manage.py shell -c "from rest_framework.authtoken.models import Token; from api.models import User; token = Token.objects.create(user=User.objects.get(id=2),key='1d18b962d6f976b0b7e8fcf9fcc39b56cf278051'); print('Token for c2@example.com'); print(token)"

python manage.py index_facilities
