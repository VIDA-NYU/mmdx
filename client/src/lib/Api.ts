
const API_URL = "/api/v1"

export interface Hits {
    total: number;
    hits: Hit[];
}

export interface Hit {
    image: string;
    title: string;
    score: number;
}

interface ApiHit {
    _distance: number;
    image_path: string;
}

interface ApiHits {
    total: number;
    hits: ApiHit[]
}

function toHits(response: ApiHits): Hits {
    let hits: Hit[] = [];
    for (let i = 0; i < response.hits.length; i++) {
        const h = response.hits[i];
        hits.push({
            title: h.image_path,
            image: h.image_path,
            score: h._distance,
        });
    }
    return { total: hits.length, hits };
}

export async function search(queryStr: string, limit: number): Promise<Hits> {

    const response = await fetchJSON("/keyword_search", {
        "q": queryStr,
        limit: limit.toString(),
    }).catch((e) => {
        throw new Error("Failed to retrieve search results.", { cause: e })
    }) as ApiHits;

    return toHits(response);
}

export async function similar(imagePath: string, limit: number): Promise<Hits> {
    const response = await fetchJSON("/image_search", {
        "q": imagePath,
        limit: limit.toString(),
    }).catch((e) => {
        throw new Error("Failed to search for similar images.", { cause: e })
    }) as ApiHits;
    return toHits(response);
}

export async function random(limit: number): Promise<Hits> {

    const response = await fetchJSON("/random", {
        limit: limit.toString(),
    }).catch((e) => {
        throw new Error("Failed to retrieve random results.", { cause: e })
    }) as ApiHits;

    return toHits(response);
}

interface FetchInit {
    method: string;
    headers: { [index: string]: string };
    body?: string;
    credentials: 'include';
}

export function fetchJSON(
    url: string,
    args?: { [key: string]: any } | null,
    post?: object | null,
    external?: boolean,
) {
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
