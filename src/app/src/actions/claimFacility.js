import { createAction } from 'redux-act';

import apiRequest from '../util/apiRequest';

import {
    logErrorAndDispatchFailure,
    makeGetFacilityByOARIdURL,
    makeParentCompanyOptionsAPIURL,
    mapDjangoChoiceTuplesToSelectOptions,
} from '../util/util';

export const startFetchClaimFacilityData = createAction(
    'START_FETCH_CLAIM_FACILITY_DATA',
);
export const failFetchClaimFacilityData = createAction(
    'FAIL_FETCH_CLAIM_FACILITY_DATA',
);
export const completeFetchClaimFacilityData = createAction(
    'COMPLETE_FETCH_CLAIM_FACILITY_DATA',
);
export const clearClaimFacilityDataAndForm = createAction(
    'CLEAR_CLAIM_FACILITY_DATA_AND_FORM',
);

export function fetchClaimFacilityData(oarID) {
    return dispatch => {
        dispatch(startFetchClaimFacilityData());

        return apiRequest
            .get(makeGetFacilityByOARIdURL(oarID))
            .then(({ data }) => dispatch(completeFetchClaimFacilityData(data)))
            .catch(err =>
                dispatch(
                    logErrorAndDispatchFailure(
                        err,
                        'An error prevented fetching data about that facility',
                        failFetchClaimFacilityData,
                    ),
                ),
            );
    };
}

export const updateClaimAFacilityContactPerson = createAction(
    'UPDATE_CLAIM_A_FACILITY_CONTACT_PERSON',
);
export const updateClaimAFacilityJobTitle = createAction(
    'UPDATE_CLAIM_A_FACILITY_JOB_TITLE',
);
export const updateClaimAFacilityEmail = createAction(
    'UPDATE_CLAIM_A_FACILITY_EMAIL',
);
export const updateClaimAFacilityPhoneNumber = createAction(
    'UPDATE_CLAIM_A_FACILITY_PHONE_NUMBER',
);
export const updateClaimAFacilityCompany = createAction(
    'UPDATE_CLAIM_A_FACILITY_COMPANY',
);
export const updateClaimAFacilityParentCompany = createAction(
    'UPDATE_CLAIM_A_FACILITY_PARENT_COMPANY',
);
export const updateClaimAFacilityWebsite = createAction(
    'UPDATE_CLAIM_A_FACILITY_WEBSITE',
);
export const updateClaimAFacilityDescription = createAction(
    'UPDATE_CLAIM_A_FACILITY_DESCRIPTION',
);
export const updateClaimAFacilityVerificationMethod = createAction(
    'UPDATE_CLAIM_A_FACILITY_VERIFICATION_METHOD',
);
export const updateClaimAFacilityPreferredContactMethod = createAction(
    'UPDATE_CLAIM_A_FACILITY_PREFERRED_CONTACT_METHOD',
);
export const updateClaimAFacilityLinkedinProfile = createAction(
    'UPDATE_CLAIM_A_FACILITY_LINKEDIN_PROFILE',
);

export const startFetchParentCompanyOptions = createAction(
    'START_FETCH_PARENT_COMPANY_OPTIONS',
);
export const failFetchParentCompanyOptions = createAction(
    'FAIL_FETCH_PARENT_COMPANY_OPTIONS',
);
export const completeFetchParentCompanyOptions = createAction(
    'COMPLETE_FETCH_PARENT_COMPANY_OPTIONS',
);
export const resetParentCompanyOptions = createAction(
    'RESET_PARENT_COMPANY_OPTIONS',
);

export function fetchParentCompanyOptions() {
    return dispatch => {
        dispatch(startFetchParentCompanyOptions());

        return apiRequest
            .get(makeParentCompanyOptionsAPIURL())
            .then(({ data }) => mapDjangoChoiceTuplesToSelectOptions(data))
            .then(data => dispatch(completeFetchParentCompanyOptions(data)))
            .catch(err =>
                dispatch(
                    logErrorAndDispatchFailure(
                        err,
                        'An error prevented fetching parent company / supplier group options',
                        failFetchParentCompanyOptions,
                    ),
                ),
            );
    };
}
