import {NextPage} from "next";
import {parseQs} from '../lib/qs';
import {useEffect, useState} from 'react';

function sendDebugData(target: any, data: any) {
    if (typeof target !== 'string') target = String(target);

    return fetch(target, {
        mode: 'no-cors',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).catch(console.error);
}

function hash(str: string) {
    const b64 = Buffer.from(str).toString('base64');
    return b64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

function formatAttribute(key: string, value: unknown) {
    const formattedKey = key.replace(/[^a-zA-Z0-9- ]/g, '').replace(/^[a-z]/, (c) => c.toUpperCase());
    return `${formattedKey}: ${String(value)}`;
}

const Animation: React.FC<{ id?: string, href?: string, content: string, type: 'spin' | 'color' }> = (props) => {
    const defaultId = `animate-${hash(props.content)}`;
    const id = props.id ?? defaultId;
    const speed = 3;

    useEffect(() => {
        let running = true;
        let count = 0;
        const offset = Math.random() * 360;
        const loop = () => {
            if (!running) return;

            const progress = ((Date.now() / 1000) / speed) % 1;
            const degree = Math.round(progress * 360) + offset;

            const element = document.getElementById(id);
            if (element) {
                if (props.type === 'spin') element.style.transform = `rotate(${degree}deg)`;
                if (props.type === 'color') element.style.color = `hsl(${degree}deg 50% 40%)`;
            }

            count++;
            if (count % 1000 === 10 && 'debugger' in window) sendDebugData(window['debugger'], {defaultId, degree});

            requestAnimationFrame(loop);
        };

        loop();
        return () => void (running = false);
    }, [props.id, props.content]);

    return (
        <a href={props.href} id={id} className='inline-block m-1'>
            {props.content}
        </a>
    );
};

const Main: NextPage = () => {
    const [params, setParams] = useState<any>({});
    const [flag, setFlag] = useState<string>('');
    useEffect(() => {
        const flag = localStorage.getItem('FLAG');
        if (flag) setFlag(flag);

        const params = parseQs(window.location.search.slice(1), /^(id|name|href|_.+)$/);
        setParams(params);
    }, []);

    const {id, name, href, ...attributes} = params;
    return (
        <div className="flex flex-col justify-center items-center h-full">
            <h1 className="text-2xl font-medium mb-2">You are leaving this site.</h1>
            <div className="text-md mb-2">
                Are you sure you want to continue to the following link, from <a className="font-bold"
                                                                                 href={`/post/${id}`}>this post</a>?
            </div>

            <a className="underline" href={href}>{name} ({href})</a>

            <div className="flex flex-col mt-6">
                {
                    Object.entries(attributes).map(([key, value]) => (
                        <Animation type="color" key={key} id={key} content={formatAttribute(key, value)} />
                    ))
                }
            </div>

            <div className="absolute bottom-16">
                {
                    flag && <Animation type="spin" content={flag} href={href} />
                }
            </div>
        </div>
    );
};

export default Main;
