import React, { useEffect } from 'react';
import { Html5Qrcode } from 'html5-qrcode';

export default function WebQRCodeScanner() {
    const handleQRCodeScanned = (data: string) => {
        console.log('Scanned QR Code:', data);
    };

    useEffect(() => {
        const qrCodeScanner = new Html5Qrcode('reader');
        qrCodeScanner.start(
            { facingMode: 'environment' },
            {
                fps: 10,
            },
            (decodedText) => handleQRCodeScanned(decodedText),
            () => { }
        );

        return () => {
            qrCodeScanner.stop().catch(console.warn);
        };
    }, []);

    return <div id="reader" style={{ width: '100%', height: '100%' }} />;
}