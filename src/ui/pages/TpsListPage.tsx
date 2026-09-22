import * as React from 'react';
import { useState } from 'react';

import {
    K8sResourceCommon,
    ListPageBody,
    ListPageHeader,
    ResourceLink,
    RowProps,
    TableColumn,
    TableData,
    Timestamp,
    VirtualizedTable,
} from '@openshift-console/dynamic-plugin-sdk';

import {
    TERMINATED_POD_SNAPSHOT_GVK,
    NS_GVK,
    TerminatedPodSnapshot,
} from '../utilities/objectDefs';

import { sortable, SortByDirection } from '@patternfly/react-table';

import TpsK8sUtils from '../utilities/tpsK8sUtils';
import { Switch, Toolbar, ToolbarContent, ToolbarItem } from '@patternfly/react-core';

type TerminatedPodSnapshotTableProps = {
    data: K8sResourceCommon[];
    unfilteredData: K8sResourceCommon[];
    loaded: boolean;
    loadError: any;
};

const TerminatedPodSnapshotsTable: React.FC<TerminatedPodSnapshotTableProps> = ({ data, unfilteredData, loaded, loadError }) => {

    const columns: TableColumn<K8sResourceCommon>[] = [
        {
            title: 'Name',
            id: 'name',
            sort: 'metadata.name',
            transforms: [sortable],
        },
        {
            title: 'Namespace',
            id: 'namespace',
            sort: 'metadata.namespace',
            transforms: [sortable],
        },
        {
            title: 'Restarts',
            id: 'restarts',
            sort: (data: K8sResourceCommon[], direction: SortByDirection) => [...data].sort((a, b) => {
                const atps = a as TerminatedPodSnapshot;
                const btps = b as TerminatedPodSnapshot;
                const av = atps.data.onRestartLogs ? 1 : 0;
                const bv = btps.data.onRestartLogs ? 1 : 0;
                const cmp = av - bv; // 0 = empty first, 1 = non-empty first
                return direction === SortByDirection.asc ? cmp : -cmp;
            }),
            transforms: [sortable],
        },
        {
            title: 'Deleted',
            id: 'deleted',
            sort: (data: K8sResourceCommon[], direction: SortByDirection) => [...data].sort((a, b) => {
                const atps = a as TerminatedPodSnapshot;
                const btps = b as TerminatedPodSnapshot;
                const av = atps.data.onDeleteLogs ? 1 : 0;
                const bv = btps.data.onDeleteLogs ? 1 : 0;
                const cmp = av - bv; // 0 = empty first, 1 = non-empty first
                return direction === SortByDirection.asc ? cmp : -cmp;
            }),
            transforms: [sortable],
        },
        {
            title: 'Phase',
            id: 'phase',
            sort: 'data.status.phase',
            transforms: [sortable],
        },
        {
            title: 'Error',
            id: 'error',
            sort: (data: K8sResourceCommon[], direction: SortByDirection) => [...data].sort((a, b) => {
                const atps = a as TerminatedPodSnapshot;
                const btps = b as TerminatedPodSnapshot;
                const av = (atps.data.onRestartLogs || atps.data.status?.phase != 'Succeeded') ? 1 : 0;
                const bv = (btps.data.onRestartLogs || btps.data.status?.phase != 'Succeeded') ? 1 : 0;
                const cmp = av - bv; // 0 = empty first, 1 = non-empty first
                return direction === SortByDirection.asc ? cmp : -cmp;
            }),
            transforms: [sortable],
        },
        {
            title: 'Created',
            id: 'created',
            sort: 'metadata.creationTimestamp',
            transforms: [sortable],
        },
    ];

    const TerminatedPodSnapshotRow: React.FC<RowProps<K8sResourceCommon>> = ({ obj, activeColumnIDs }) => {
        const tps: TerminatedPodSnapshot = obj as TerminatedPodSnapshot;

        return (
            <>
                <TableData id={columns[0].id} activeColumnIDs={activeColumnIDs}>
                    <ResourceLink groupVersionKind={TERMINATED_POD_SNAPSHOT_GVK}
                                  name={tps.metadata?.name}
                                  namespace={tps.metadata?.namespace}>
                    </ResourceLink>
                </TableData>
                <TableData id={columns[1].id} activeColumnIDs={activeColumnIDs}>
                    <ResourceLink groupVersionKind={NS_GVK} name={tps.metadata?.namespace} />
                </TableData>
                <TableData id={columns[2].id} activeColumnIDs={activeColumnIDs}>
                    {tps.data.onRestartLogs ? 'YES' : ''}
                </TableData>
                <TableData id={columns[3].id} activeColumnIDs={activeColumnIDs}>
                    {tps.data.onDeleteLogs ? 'YES' : ''}
                </TableData>
                <TableData id={columns[4].id} activeColumnIDs={activeColumnIDs}>
                    {tps.data?.status?.phase || '-'}
                </TableData>
                <TableData id={columns[5].id} activeColumnIDs={activeColumnIDs}>
                    {(tps.data.onRestartLogs || tps.data.status?.phase != 'Succeeded') ? 'YES' : ''}
                </TableData>
                <TableData id={columns[6].id} activeColumnIDs={activeColumnIDs}>
                    <Timestamp timestamp={tps.metadata?.creationTimestamp || '-'} />
                </TableData>
            </>
        );
    };

    return (
        <VirtualizedTable<K8sResourceCommon>
            data={data}
            unfilteredData={unfilteredData}
            loaded={loaded}
            loadError={loadError}
            columns={columns}
            Row={TerminatedPodSnapshotRow}
        />
    );
}

export const TpsListPage = (model: { namespace: any; }) => {

    const [isChecked, setIsChecked] = useState<boolean>(false);
    const [tpss, loaded, loadError] = TpsK8sUtils.getTerminatedPodSnapshots({namespace: model.namespace});

    const handleChange = (_event: React.FormEvent<HTMLInputElement>, checked: boolean) => {
        setIsChecked(checked);
    };

    let filteredTpss = isChecked ? tpss : tpss.filter(tps =>
        tps.data.onRestartLogs || tps.data.status?.phase !== 'Succeeded'
    );

    return (
        <>
            <ListPageHeader title={'Ahplos TerminatedPodSnapshots'}/>
            <ListPageBody>
                <Toolbar inset={{ default: 'insetLg' }} hasNoPadding>
                    <ToolbarContent>
                        <ToolbarItem align={{ default: 'alignEnd' }}>
                            <Switch
                                id="show-nominal"
                                label="Show Nominal"
                                isChecked={isChecked}
                                onChange={handleChange}
                            />
                        </ToolbarItem>
                    </ToolbarContent>
                </Toolbar>
                <TerminatedPodSnapshotsTable
                    data={filteredTpss}
                    unfilteredData={tpss}
                    loaded={loaded}
                    loadError={loadError}
                />
            </ListPageBody>
        </>
    );
};

export default TpsListPage;