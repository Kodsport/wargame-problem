import {NextPage} from "next";
import {useRouter} from 'next/router';
import {useState} from 'react';

const Link: React.FC<{ id: string, name: string, href: string, attributes: Record<string, string> }> = (props) => {
    const {children, attributes, name, ...rest} = props;
    const qs = new URLSearchParams({...rest, ...attributes}).toString();

    return (
        <a className="underline" href={'/redirect?' + qs}>{name}</a>
    );
};

interface Post {
    title: string;
    content: string;
    links: { name: string, href: string, attributes: Record<string, string> }[];
}

function getPost(id: string): Post {
    const decoded = atob(id.replace(/_/g, '/').replace(/-/g, '+'));
    return JSON.parse(decoded);
}

const Main: NextPage = ({  }) => {
    const [auditDisabled, setAuditDisabled] = useState(false);

    const router = useRouter();
    if (typeof router.query.id !== 'string') return null;

    const id = router.query.id as string;
    const post = getPost(id);
    return (
        <div className="flex flex-col justify-center items-center w-full h-full">
            <div className="flex flex-col justify-center items-start w-4/12">
                <h1 className="text-3xl font-medium mb-4">{post.title}</h1>
                <p className="text-sm mb-2">{post.content}</p>

                <div className="mt-8">
                    <h2 className="text-xl font-medium mb-3">Sources</h2>
                    <ul>
                        {
                            post.links.map((link, index) => (
                                <li className="mb-1">
                                    <Link key={index} id={id} name={link.name} href={link.href}
                                          attributes={link.attributes}/>
                                </li>
                            ))
                        }
                    </ul>
                </div>

                <div className="absolute bottom-16 left-16">
                    <button
                        className="text-blue-500 hover:underline disabled:opacity-50"
                        disabled={auditDisabled}
                        onClick={() => {
                            if (auditDisabled) return;
                            setAuditDisabled(true);

                            fetch('/api/audit', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    postId: id
                                }),
                            })
                                .then(res => {
                                    if (!res.ok) return alert('Failed to send audit request');
                                    alert('Your audit was successfull');
                                })
                                .catch(() => alert('Failed to audit the post'))
                                .finally(() => setAuditDisabled(false));
                        }}
                    >
                        Audit
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Main;
