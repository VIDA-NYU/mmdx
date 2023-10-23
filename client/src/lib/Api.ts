const API_URL = "/api/v1"

export interface Hits {
    total: number;
    hits: Hit[];
}

export interface Hit {
    _distance: number;
    image_path: string;
    labels?: string[];
}

export async function keywordSearch(queryStr: string, limit: number): Promise<Hits> {
    const response = await fetchJSON<Hits>("/keyword_search", {
        "q": queryStr,
        limit: limit.toString(),
    }).catch((e) => {
        throw new Error("Failed to retrieve keyword search results.", { cause: e })
    });
    return response;
}

export async function similarSearch(imagePath: string, limit: number): Promise<Hits> {
    const response = await fetchJSON<Hits>("/image_search", {
        "q": imagePath,
        limit: limit.toString(),
    }).catch((e) => {
        throw new Error("Failed to search for similar images.", { cause: e })
    });
    return response;
}

export async function random(limit: number): Promise<Hits> {
    const response = await fetchJSON<Hits>("/random", {
        limit: limit.toString(),
    }).catch((e) => {
        throw new Error("Failed to retrieve random search results.", { cause: e })
    });
    return response;
}

interface LabelsResponse {
    labels: string[];
}

export async function loadLabels(): Promise<LabelsResponse> {
    const response = await fetchJSON<LabelsResponse>("/labels").catch((e) => {
        throw new Error("Failed to load labels.", { cause: e })
    });
    return response;
}

interface AddLabelResponse {
    success: boolean;
}

export async function addLabel(image_path: string, label: string): Promise<AddLabelResponse> {
    const response = await fetchJSON<AddLabelResponse>("/add_label", {
        image_path,
        label
    }).catch((e) => {
        throw new Error("Failed to save label.", { cause: e })
    });
    return response;
}

interface RemoveLabelResponse {
    success: boolean;
}

export async function removeLabel(image_path: string, label: string): Promise<AddLabelResponse> {
    const response = await fetchJSON<RemoveLabelResponse>("/remove_label", {
        image_path,
        label
    }).catch((e) => {
        throw new Error("Failed to remove label.", { cause: e })
    });
    return response;
}

export function downloadFile() {
    const url = `${API_URL}/download/binary_labeled_data`
    const link = document.createElement('a');
    link.href = url;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


interface FetchInit {
    method: string;
    headers: { [index: string]: string };
    body?: string;
    credentials: 'include';
}

export function fetchJSON<T>(
    url: string,
    args?: { [key: string]: any } | null,
    post?: object | null,
    external?: boolean,
): Promise<T> {
    let argstring = '';
    if (args) {
        Object.keys(args).forEach((k, ix) => {
            const kk = encodeURIComponent(k);
            const ak = args[k] !== undefined ? encodeURIComponent(args[k]) : '';
            argstring += `${ix === 0 ? '?' : '&'}${kk}=${ak}`;
        });
    }
    const init: FetchInit = {
        method: post ? 'POST' : 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    };

    if (post) {
        const content = JSON.stringify(post, null, '');
        init.headers['Content-Length'] = `${content.length}`;
        init.body = content;
    }
    const path = external ? url : `${API_URL}${url}${argstring}`;
    return fetch(path, init)
        .then(data => {
            if (data.status !== 200 || !data.ok) {
                throw new Error(`Server returned ${data.status}${data.ok ? ' ok' : ''}`);
            }
            const ct = data.headers.get('content-type');
            if (ct && ct.includes('application/json')) {
                return data.json();
            }
            throw new TypeError('Response is not JSON encoded');
        });
}
