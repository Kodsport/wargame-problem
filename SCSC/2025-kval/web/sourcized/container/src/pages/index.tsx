import {NextPage} from "next";
import {useState} from 'react';
import {useRouter} from 'next/router';

const Main: NextPage = () => {
    const router = useRouter();

    const [title, setTitle] = useState<string>('');
    const [content, setContent] = useState<string>('');

    const [sources, setSources] = useState<string[]>([]);
    return (
        <div className="flex flex-col justify-center items-center h-full w-full">
            <div className="flex flex-col justify-center items-center h-full w-8/12">
                <h1 className="text-2xl font-medium mb-6">Write your own paper here!</h1>

                <div className="flex flex-col items-center w-full mb-6">
                    <div className="flex flex-col w-full">
                        <div className="flex flex-col mb-6">
                            <label htmlFor="title"
                                   className="block mb-2 text-sm font-medium text-gray-900">Title</label>
                            <input
                                type="text"
                                id="title"
                                value={title}
                                onChange={e => setTitle(e.target.value)}

                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                placeholder="My best paper"
                                required
                            />
                        </div>
                        <div className="flex flex-col mb-6">
                            <label htmlFor="content"
                                   className="block mb-2 text-sm font-medium text-gray-900">Content</label>
                            <textarea
                                id="content"
                                value={content}
                                onChange={e => setContent(e.target.value)}

                                rows={8}

                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                placeholder="My best paper"
                                required
                            />
                        </div>
                    </div>

                    <div className="w-full">
                        <p className="block mb-2 text-sm font-medium text-gray-900">Sources</p>
                        <ul className="mb-4" id="sources">
                            {
                                sources.map((source, index) => (
                                    <li key={index} className="w-full flex flex-row mb-2">
                                        <input
                                            type="text"
                                            value={source}
                                            onChange={e => {
                                                const newSources = [...sources];
                                                newSources[index] = e.target.value;
                                                setSources(newSources);
                                            }}

                                            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                            placeholder="https://example.com"
                                            required
                                        />
                                        <button
                                            onClick={() => {
                                                const newSources = [...sources];
                                                newSources.splice(index, 1);
                                                setSources(newSources);
                                            }}

                                            className="bg-white border border-red-500 text-white-900 rounded-lg hover:bg-red-500 block ml-2 p-2.5"
                                        >
                                            <img className="w-6 h-6 scale-110" src="/close.svg" alt="close"/>
                                        </button>
                                    </li>
                                ))
                            }
                        </ul>

                        <button
                            onClick={() => setSources(sources => [...sources, ''])}
                            className="bg-white border border-blue-400 text-blue-600 font-medium text-sm rounded-lg hover:text-white hover:bg-blue-400 block py-2 px-4"
                        >
                            Add source
                        </button>
                    </div>
                </div>

                <div className="flex flex-row w-full mt-2">
                    <button
                        onClick={() => {
                            const data = {
                                title,
                                content,
                                links: sources.map(source => ({name: source, href: source, attributes: {}})),
                            };

                            const encoded = btoa(JSON.stringify(data)).replace(/=/g, '').replace(/\//g, '_').replace(/\+/g, '-');
                            return router.push(`/post/${encoded}`);
                        }}
                        className="bg-white border border-green-400 text-green-600 font-medium text-sm rounded-lg hover:text-white hover:bg-green-400 block py-2 px-4 w-48"
                    >
                        Preview
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Main;
