import '../../styles/globals.css'
import type {AppProps} from 'next/app'
import React from 'react';
import Head from 'next/head';

function App({ Component, pageProps }: AppProps) {
    return (
        <>
            <Head>
                <title>Something</title>

                <meta name="viewport" content="initial-scale=1.0, width=device-width" />
                <meta name="theme-color" content="#FEFEFE" />

                <base href="/" />
            </Head>
            <Component {...pageProps} />
        </>
    );
}

export default App