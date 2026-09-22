import {
    K8sResourceKind,
    useK8sWatchResource,
    WatchK8sResource
} from '@openshift-console/dynamic-plugin-sdk';

import {
    TERMINATED_POD_SNAPSHOT_GVK,
    TerminatedPodSnapshot
} from './objectDefs'

export class InvalidK8sSingleResourceQueryError extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'InvalidK8sSingleResourceQueryError';
    }
}

export default class TpsK8sUtils {

    private static getK8sResource<T extends K8sResourceKind> (options: WatchK8sResource = {}):
        [T, boolean, string]
    {
        let [results, loaded, errorMsg] = useK8sWatchResource<T>(options);

        return [results as T, loaded, errorMsg];
    }

    private static getK8sResources<T extends K8sResourceKind[]> (options: WatchK8sResource = {}):
         [T, boolean, string]
    {
        let [results, loaded, errorMsg] = useK8sWatchResource<T>(options);

        return [results, loaded, errorMsg];
    }

    public static getTerminatedPodSnapshot (options: WatchK8sResource = {}):
        [TerminatedPodSnapshot, boolean, string]
    {
        options.groupVersionKind = TERMINATED_POD_SNAPSHOT_GVK;
        return TpsK8sUtils.getK8sResource(options);
    }

    public static getTerminatedPodSnapshots (options: WatchK8sResource = {}):
        [TerminatedPodSnapshot[], boolean, string]
    {
        options.groupVersionKind = TERMINATED_POD_SNAPSHOT_GVK;
        options.isList = true;
        return TpsK8sUtils.getK8sResources<TerminatedPodSnapshot[]>(options);
    }
}
