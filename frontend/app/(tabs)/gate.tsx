import React, { useState } from 'react';
import { CameraView, useCameraPermissions, BarcodeScanningResult } from 'expo-camera';
import { ActivityIndicator, View, StyleSheet, Text, Button } from 'react-native';
import Icon from "react-native-vector-icons/FontAwesome";
import { verifyProof, verifyPublicKey } from '@/utils';
import { zkContract } from "@/constants/contracts";

export default function WebQRCodeScanner() {
    const [isLoading, setIsLoading] = useState(false);
    const [isVerified, setIsVerified] = useState<null | boolean>(null);
    const [permission, requestPermission] = useCameraPermissions();

    const handleQRCodeScanned = async (data: BarcodeScanningResult) => {
        setIsLoading(true);
        // Dummy data for testing
        if (verifyProof(23, 5, 8, 19, 3, 6)) {
            await verifyPublicKey(8);
            await zkContract.invalidatePublicKey(8);
            // TODO: send invalidation ID to the server
            setIsVerified(true);
        } else {
            setIsVerified(false);
        }
        setTimeout(() => setIsVerified(null), 2000);
        setIsLoading(false);
    };

    if (!permission) {
        // Camera permissions are still loading.
        return <View />;
    }

    if (!permission.granted) {
        // Camera permissions are not granted yet.
        return (
            <View style={styles.container}>
                <Text style={styles.message}>We need your permission to show the camera</Text>
                <Button onPress={requestPermission} title="grant permission" />
            </View>
        );
    }

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

        <CameraView style={styles.camera} facing='back' barcodeScannerSettings={{ barcodeTypes: ["qr"] }} onBarcodeScanned={handleQRCodeScanned}>
            <View style={styles.buttonContainer} />
        </CameraView>
    </View>
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
    },
    message: {
        textAlign: 'center',
        paddingBottom: 10,
    },
    camera: {
        flex: 1,
    },
    buttonContainer: {
        flex: 1,
        flexDirection: 'row',
        backgroundColor: 'transparent',
        margin: 64,
    },
    button: {
        flex: 1,
        alignSelf: 'flex-end',
        alignItems: 'center',
    },
    text: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
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
    }
});