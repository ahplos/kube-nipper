import {
    K8sGroupVersionKind,
    K8sResourceCommon
} from "@openshift-console/dynamic-plugin-sdk";

export const BATCH_AHPLOS_ORG = "monitoring.ahplos.org";
export const API_VERSION = "v1beta1";

export const NS_GVK: K8sGroupVersionKind = {
    kind: "Namespace",
    version: "v1"
};

export const TERMINATED_POD_SNAPSHOT_GVK: K8sGroupVersionKind = {
    group: BATCH_AHPLOS_ORG,
    version: API_VERSION,
    kind: "TerminatedPodSnapshot",
};

export type Event = {
    lastTimestamp: string;
    message: string;
    reason: string;
    reportingComponent: string;
    type: string;
}

export type TerminatedPodSnapshot = K8sResourceCommon & {
    data: {
        events: Event[];
        onDeleteLogs: {
            container: string;
            timeCollected: string;
            logs: string;
        }
        onRestartLogs: {
            container: string;
            timeCollected: string;
            logs: string;
        }
        spec: Record<string, unknown>;
        status: Record<string, unknown>;
    };
};