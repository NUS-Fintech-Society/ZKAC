import React, { useState } from 'react';
import { TouchableOpacity, StyleSheet, ToastAndroid, Alert, Platform, ActivityIndicator } from 'react-native';
import QRCode from 'react-native-qrcode-svg';
import CryptoJS from 'crypto-js';
import { ThemedView } from '@/components/ThemedView';
import { ThemedText } from '@/components/ThemedText';
import { g, p } from '@/constants/contracts';

export default function Authentication() {
  const [proofData, setProofData] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const generateProof = async () => {
    setLoading(true);
    try {
      const x = Math.floor(Math.random() * 100);
      const r = Math.floor(Math.random() * 100);

      const a = BigInt(g) ** BigInt(r) % BigInt(p);
      const y = BigInt(g) ** BigInt(x) % BigInt(p);
      const e = parseInt(CryptoJS.SHA256(a.toString() + y.toString()).toString(), 16) % (p - 1);
      const s = (r + e * x) % (p - 1);

      const invalidationID = CryptoJS.SHA256(Math.random().toString()).toString();
      const proof = { a: a.toString(), s: s.toString(), y: y.toString(), invalidationID };

      setProofData(JSON.stringify(proof));
      setTimeout(() => setProofData(null), 300000); // Clear after 5 minutes

      if (Platform.OS === 'android') {
        ToastAndroid.show("Proof generated successfully!", ToastAndroid.SHORT);
      } else {
        Alert.alert("Proof generated successfully!");
      }
    } catch (error) {
      // Check if error is an instance of Error before accessing message
      if (error instanceof Error) {
        Alert.alert("Error generating proof", error.message);
      } else {
        Alert.alert("Error generating proof", "An unknown error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <ThemedText style={styles.title}>Authentication</ThemedText>
      <ThemedText style={styles.description}>Generate and share your proof securely</ThemedText>

      {loading && <ActivityIndicator size="large" color="#4a90e2" />}

      <TouchableOpacity style={styles.button} onPress={generateProof} disabled={loading}>
        <ThemedText style={styles.buttonText}>Generate Proof</ThemedText>
      </TouchableOpacity>

      {proofData && (
        <ThemedView style={styles.qrContainer}>
          <ThemedText style={styles.qrText}>Scan QR Code to Authenticate</ThemedText>
          <QRCode value={proofData} size={200} />
          <TouchableOpacity style={styles.clearButton} onPress={() => setProofData(null)}>
            <ThemedText style={styles.clearButtonText}>Clear QR Code</ThemedText>
          </TouchableOpacity>
        </ThemedView>
      )}
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f0f4f7',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  description: {
    fontSize: 18,
    color: '#666',
    marginBottom: 30,
    textAlign: 'center',
    paddingHorizontal: 20,
  },
  button: {
    backgroundColor: '#4a90e2',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    marginBottom: 20,
    shadowColor: '#4a90e2',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  qrContainer: {
    alignItems: 'center',
    marginTop: 20,
    padding: 15,
    backgroundColor: '#fff',
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 4,
  },
  qrText: {
    fontSize: 16,
    color: '#333',
    marginBottom: 15,
  },
  clearButton: {
    backgroundColor: '#d9534f',
    paddingVertical: 8,
    paddingHorizontal: 20,
    borderRadius: 6,
    marginTop: 15,
  },
  clearButtonText: {
    color: '#fff',
    fontSize: 14,
  },
});