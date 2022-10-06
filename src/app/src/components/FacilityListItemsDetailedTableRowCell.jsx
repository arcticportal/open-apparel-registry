import React, { Fragment } from 'react';
import {
    arrayOf,
    bool,
    func,
    number,
    oneOf,
    oneOfType,
    shape,
    string,
} from 'prop-types';
import Typography from '@material-ui/core/Typography';
import get from 'lodash/get';

import CellElement from './CellElement';
import ShowOnly from './ShowOnly';

import { facilityMatchStatusChoicesEnum } from '../util/constants';

import { confirmRejectMatchRowStyles } from '../util/styles';

export default function FacilityListItemsDetailedTableRowCell({
    title,
    subtitle,
    stringIsHidden,
    data,
    hasActions,
    fetching,
    errorState,
    linkURLs,
    readOnly,
    isRemoved,
}) {
    const statusSection = (() => {
        if (isRemoved) {
            return 'REMOVED';
        }

        return title;
    })();

    return (
        <>
            {statusSection}
            <ShowOnly when={!readOnly}>
                <div style={confirmRejectMatchRowStyles.cellSubtitleStyles}>
                    <Typography variant="body2">{subtitle}</Typography>
                </div>
                {data.map((item, index) => (
                    <Fragment key={item.id ? item.id : item}>
                        <CellElement
                            item={item}
                            fetching={fetching}
                            errorState={errorState}
                            hasActions={hasActions}
                            stringIsHidden={stringIsHidden}
                            linkURL={get(linkURLs, [`${index}`], null)}
                        />
                    </Fragment>
                ))}
            </ShowOnly>
        </>
    );
}

FacilityListItemsDetailedTableRowCell.defaultProps = {
    stringIsHidden: false,
    hasActions: false,
    fetching: false,
    subtitle: ' ',
    errorState: false,
    linkURLs: null,
    readOnly: false,
    isRemoved: false,
};

FacilityListItemsDetailedTableRowCell.propTypes = {
    title: oneOfType([number, string]).isRequired,
    subtitle: string,
    stringIsHidden: bool,
    data: oneOfType([
        arrayOf(number.isRequired),
        arrayOf(string.isRequired),
        arrayOf(
            shape({
                id: number.isRequired,
                confirmMatch: func.isRequired,
                rejectMatch: func.isRequired,
                status: oneOf(Object.values(facilityMatchStatusChoicesEnum))
                    .isRequired,
                matchName: string.isRequired,
                matchAddress: string.isRequired,
                itemName: string.isRequired,
                itemAddress: string.isRequired,
            }),
        ).isRequired,
    ]).isRequired,
    hasActions: bool,
    fetching: bool,
    errorState: bool,
    linkURLs: arrayOf(string),
    readOnly: bool,
    isRemoved: bool,
};
