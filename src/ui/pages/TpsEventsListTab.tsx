import * as React from 'react';
import { useState } from 'react';

import {
    RowProps,
    TableColumn,
    TableData,
    Timestamp,
    VirtualizedTable,
} from '@openshift-console/dynamic-plugin-sdk';

import {
    Switch,
    TabContent,
    TabContentBody,
    Toolbar,
    ToolbarContent,
    ToolbarItem
} from '@patternfly/react-core';

import {
    Event,
    TerminatedPodSnapshot
} from '../utilities/objectDefs';

import { sortable } from '@patternfly/react-table';

type TerminatedPodSnapshotTableProps = {
    data: Event[];
    unfilteredData: Event[];
    loaded: boolean;
    loadError: any;
};

const TerminatedPodSnapshotEventsTable: React.FC<TerminatedPodSnapshotTableProps> = ({ data, unfilteredData, loaded, loadError }) => {

    const columns: TableColumn<Event>[] = [
        {
            title: 'Time',
            id: 'last-time-stamp',
            sort:'lastTimestamp',
            transforms: [sortable],
        },
        {
            title: 'Type',
            id: 'type',
            sort: 'type',
            transforms: [sortable],
        },
        {
            title: 'Reporting Component',
            id: 'reporting-component',
            sort: 'reportingComponent',
            transforms: [sortable],
        },
        {
            title: 'Reason',
            id: 'reason',
            sort: 'reason',
            transforms: [sortable],
        },
        {
            title: 'Message',
            id: 'message',
            sort: 'message',
            transforms: [sortable],
        },
    ];

    const TerminatedPodSnapshotEventRow: React.FC<RowProps<Event>> = ({ obj, activeColumnIDs }) => {
        const event: Event = obj as Event;

        return (
            <>
                <TableData id={columns[0].id} activeColumnIDs={activeColumnIDs}>
                    <Timestamp timestamp={event.lastTimestamp} />
                </TableData>
                <TableData id={columns[1].id} activeColumnIDs={activeColumnIDs}>
                    {event.type}
                </TableData>
                <TableData id={columns[2].id} activeColumnIDs={activeColumnIDs}>
                    {event.reportingComponent}
                </TableData>
                <TableData id={columns[3].id} activeColumnIDs={activeColumnIDs}>
                    {event.reason}
                </TableData>
                <TableData id={columns[4].id} activeColumnIDs={activeColumnIDs}>
                    {event.message}
                </TableData>
            </>
        );
    };

    return (
        <VirtualizedTable<Event>
            data={data}
            unfilteredData={unfilteredData}
            loaded={loaded}
            loadError={loadError}
            columns={columns}
            Row={TerminatedPodSnapshotEventRow}
        />
    );
}

export const TpsEventsListTab = (model: any, page: any, component: any) => {
    let tps: TerminatedPodSnapshot = model.obj;

    const [isChecked, setIsChecked] = useState<boolean>(true);
    const handleChange = (_event: React.FormEvent<HTMLInputElement>, checked: boolean) => {
        setIsChecked(checked);
    };

    let events = isChecked ? tps.data.events.filter(ev => ev.reportingComponent != 'kopf') : tps.data.events

    return (
        <>
            <TabContent id="tps-event-tab">
                <TabContentBody hasPadding>
                    <Toolbar inset={{ default: 'insetLg' }} hasNoPadding>
                        <ToolbarContent>
                            <ToolbarItem align={{ default: 'alignEnd' }}>
                                <Switch
                                    id="show-system-events"
                                    label="Show Operator Events"
                                    isChecked={isChecked}
                                    onChange={handleChange}
                                />
                            </ToolbarItem>
                        </ToolbarContent>
                    </Toolbar>
                    <TerminatedPodSnapshotEventsTable
                        data={events}
                        unfilteredData={tps.data.events}
                        loaded={true}
                        loadError={''}
                    />
                </TabContentBody>
            </TabContent>
        </>
    );
};