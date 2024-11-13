import React from 'react';
import { StyleSheet } from 'react-native';
import Authentication from '@/components/Authentication';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function UserScreen() {
  return (
    <ThemedView style={styles.container}>
      <ThemedText style={styles.title}>User Authentication</ThemedText>
      <Authentication />
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f7f9fc', 
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333', 
    marginBottom: 20,
  },
});