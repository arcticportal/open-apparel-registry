from api.models import ExtendedField

from api.helpers import prefix_a_an


def format_download_date(date):
    return date.strftime("%Y-%m-%d")


def get_download_contribution(source, match_is_active, user_can_see_detail):
    contribution = '[Unknown Contributor]'
    is_visible = source.is_active and source.is_public and match_is_active
    source_name = "API" if source.source_type == "SINGLE" else "List"

    if source and source.contributor:
        if user_can_see_detail and is_visible:
            if source.facility_list is not None:
                source_name = source.facility_list.name
            contribution = "{} ({})".format(
                source.contributor.name,
                source_name
            )
        else:
            contribution = "{} ({})".format(
                prefix_a_an(source.contributor.contrib_type),
                source_name
            )

    return contribution


def get_download_claim_contribution(claim, user_can_see_detail):
    contribution = '[Unknown Contributor]'
    if claim and claim.contributor:
        if user_can_see_detail:
            contribution = "{} (Claimed)".format(
                claim.contributor.name
            )
        else:
            contribution = prefix_a_an(claim.contributor.contrib_type)
    return contribution


def format_download_extended_fields(fields):
    extended_fields = [
        '',
        '',
        '',
        '',
        '',
        '',
    ]
    for field in fields:
        field_name = field.get('field_name', None)
        value = field.get('value', None)
        if value is None:
            continue
        if field_name == ExtendedField.NUMBER_OF_WORKERS:
            min = value.get('min', 0)
            max = value.get('max', 0)
            extended_fields[0] = str(max) if max == min \
                else "{}-{}".format(min, max)
        elif field_name == ExtendedField.PARENT_COMPANY:
            contributor_name = value.get('contributor_name', None)
            name = value.get('name', None)
            extended_fields[1] = contributor_name \
                if contributor_name is not None else name
        elif field_name == ExtendedField.FACILITY_TYPE:
            raw_values = value.get('raw_values', [])
            extended_fields[2] = combine_raw_values(
                raw_values, extended_fields[2])

            matched_values = value.get('matched_values', [])
            extended_fields[3] = "|".join([m_value[2]
                                          for m_value in matched_values
                                          if m_value[2] is not None])
        elif field_name == ExtendedField.PROCESSING_TYPE:
            raw_values = value.get('raw_values', [])
            extended_fields[2] = combine_raw_values(
                raw_values, extended_fields[2])

            matched_values = value.get('matched_values', [])
            extended_fields[4] = "|".join([m_value[3]
                                          for m_value in matched_values
                                          if m_value[3] is not None])
        elif field_name == ExtendedField.PRODUCT_TYPE:
            raw_values = value.get('raw_values', [])
            extended_fields[5] = "|".join(value_to_set(raw_values))

    return extended_fields


def value_to_set(value):
    if isinstance(value, str):
        return set(value.split('|') if '|' in value else [value])
    return set(value)


def combine_raw_values(new_values, old_values):
    old_set = set()
    if len(old_values) != 0:
        old_set = value_to_set(old_values)
    return "|".join(
        value_to_set(new_values).union(old_set))