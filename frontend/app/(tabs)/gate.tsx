import React, { useEffect, useState } from 'react';
import { Html5Qrcode } from 'html5-qrcode';
import { ActivityIndicator, View, StyleSheet, Text } from 'react-native';
import Icon from "react-native-vector-icons/FontAwesome";

export default function WebQRCodeScanner() {
    const [isLoading, setIsLoading] = useState(false);
    const [isVerified, setIsVerified] = useState(null);

    const handleQRCodeScanned = (data: string) => {
        console.log('Scanned QR Code:', data);
        setIsLoading(true);
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

    return <View style={styles.container}>

        {isVerified !== null && (
            <View style={styles.overlay}>

                {isVerified ? (
                    <>
                        <Icon name="check-circle" size={80} color="green" />
                        <Text style={styles.verifiedText}>Verified</Text>
                    </>
                ) : (
                    <>
                        <Icon name="times-circle" size={80} color="red" />
                        <Text style={styles.unverifiedText}>Not Verified</Text>
                    </>
                )}
            </View>
        )}

        {isLoading && (
            <View style={styles.overlay}>
                <ActivityIndicator size="large" color="#ffffff" />
            </View>
        )}

        <div id="reader" style={{ width: '100%', height: '100%' }} />
    </View>
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
    },
    overlay: {
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        justifyContent: "center",
        alignItems: "center",
        zIndex: 2,
        backgroundColor: "rgba(0, 0, 0, 0.6)",
    },
    verifiedText: {
        color: "green",
        fontSize: 24,
        fontWeight: "bold",
    },
    unverifiedText: {
        color: "red",
        fontSize: 24,
        fontWeight: "bold",
    },
});