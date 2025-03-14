interface Query {
    [key: string]: string | Query | Query[];
}

// We created our own query string parser, so that we can filter out unwanted keys
export function parseQs(qs: string, regex: RegExp): Query {
    const arr = qs.split('&');
    const result: Query = {};

    for (const item of arr) {
        const [key, value] = item.split('=').map(decodeURIComponent);
        const items = key.split('[');

        let obj: Query = result;
        for (let i = 0; i < items.length; i++) {
            const objKey = items[i].replace(/]$/g, '');
            if (!regex.test(objKey)) break;

            if (i === items.length - 1) {
                obj[objKey] = value;
                continue;
            }

            if (typeof obj[objKey] !== 'object') obj[objKey] = {};
            obj = obj[objKey] as Query;
        }
    }

    return result;
}
