import React, { useState } from 'react';
import { 
  StyleSheet, View, Text, ScrollView, TouchableOpacity, 
  ActivityIndicator, Alert, Dimensions, Platform 
} from 'react-native';

import api from '../lib/api';
import { useAuthStore } from '../store/authStore';
import { 
  ArrowLeft, Globe, MapPin, Building2, 
  Sparkles, ShieldCheck, Zap, Bolt 
} from 'lucide-react-native';

const { width } = Dimensions.get('window');

export default function JobDetailScreen({ route, navigation }) {
  const { job } = route.params;
  const user = useAuthStore((s) => s.user);
  const [loading, setLoading] = useState(false);

  const handleApply = async () => {
    Alert.alert(
      "Initialize Autonomous Application?",
      `This will launch an agent to apply for ${job.title} at ${job.company}.`,
      [
        { text: "Cancel", style: "cancel" },
        { 
          text: "Launch Agent", 
          style: "default",
          onPress: async () => {
            setLoading(true);
            try {
              await api.post('/automation/apply', {
                job_id: String(job.id),
                job_url: job.url,
                resume_path: "default_resume.pdf", // Simplified
                profile_id: 1 // Simplified for demo
              });
              Alert.alert("Success", "Agent initialized. Monitor status on the Dashboard.");
              navigation.navigate('Mission Control');
            } catch (err) {
              Alert.alert("Error", "Failed to initialize agent.");
            } finally {
              setLoading(false);
            }
          }
        }
      ]
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
          <ArrowLeft color="#fff" size={24} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Job Intelligence</Text>
        <TouchableOpacity style={styles.webButton}>
          <Globe color="#737373" size={20} />
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.hero}>
          <View style={styles.companyIconLarge}>
            <Building2 color="#7c3aed" size={32} />
          </View>
          <Text style={styles.title}>{job.title}</Text>
          <Text style={styles.company}>{job.company}</Text>
          
          <View style={styles.metaRow}>
            <View style={styles.metaItem}>
              <MapPin color="#525252" size={14} />
              <Text style={styles.metaText}>{job.location}</Text>
            </View>
            <View style={styles.metaDivider} />
            <View style={styles.metaItem}>
              <Zap color="#f59e0b" size={14} />
              <Text style={styles.metaText}>{Math.round(job.match_score * 100)}% Match</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>AI Insight</Text>
          <View style={styles.insightCard}>
            <View style={styles.insightHeader}>
              <Sparkles color="#7c3aed" size={16} />
              <Text style={styles.insightTitle}>Match Analysis</Text>
            </View>
            <Text style={styles.insightText}>
                Your skills in React and Node.js are a 92% match for this role. 
                The system recommends prioritizing this application.
            </Text>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Description</Text>
          <Text style={styles.descriptionText}>{job.description}</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Skill Gap Analysis</Text>
          <View style={styles.skillsGrid}>
            {job.matched_skills?.map((skill, idx) => (
              <View key={`matched-${idx}`} style={[styles.skillBadge, styles.matchedBadge]}>
                <ShieldCheck color="#10b981" size={12} />
                <Text style={styles.skillText}>{skill}</Text>
              </View>
            ))}
            {job.missing_skills?.map((skill, idx) => (
              <View key={`missing-${idx}`} style={[styles.skillBadge, styles.missingBadge]}>
                <View style={styles.missingDot} />
                <Text style={styles.skillText}>{skill}</Text>
              </View>
            ))}
          </View>
          {job.upskill_advice && (
            <View style={styles.upskillCard}>
              <Bolt color="#f59e0b" size={14} />
              <Text style={styles.upskillText}>{job.upskill_advice}</Text>
            </View>
          )}
        </View>
        
        <View style={{ height: 100 }} />
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity 
            style={styles.applyButton} 
            onPress={handleApply}
            disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <>
              <Bolt color="#fff" size={20} />
              <Text style={styles.applyButtonText}>Autonomous Apply</Text>
            </>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 15,
    backgroundColor: '#0a0a0a',
    borderBottomWidth: 1,
    borderBottomColor: '#171717',
  },
  backButton: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  headerTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
  },
  webButton: {
    width: 40,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  scrollContent: {
    padding: 24,
  },
  hero: {
    alignItems: 'center',
    marginBottom: 32,
  },
  companyIconLarge: {
    width: 80,
    height: 80,
    borderRadius: 24,
    backgroundColor: '#171717',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#262626',
  },
  title: {
    color: '#fff',
    fontSize: 22,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  company: {
    color: '#a3a3a3',
    fontSize: 16,
    marginTop: 6,
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16,
    gap: 12,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  metaText: {
    color: '#525252',
    fontSize: 13,
    fontWeight: '500',
  },
  metaDivider: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#262626',
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    color: '#525252',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 1.5,
    marginBottom: 16,
  },
  insightCard: {
    backgroundColor: '#7c3aed08',
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: '#7c3aed20',
  },
  insightHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 10,
  },
  insightTitle: {
    color: '#a78bfa',
    fontSize: 14,
    fontWeight: 'bold',
  },
  insightText: {
    color: '#d4d4d4',
    fontSize: 14,
    lineHeight: 22,
  },
  descriptionText: {
    color: '#a3a3a3',
    fontSize: 15,
    lineHeight: 24,
  },
  skillsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  skillBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#171717',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#262626',
    gap: 6,
  },
  skillText: {
    color: '#d4d4d4',
    fontSize: 12,
    fontWeight: '600',
  },
  matchedBadge: {
    borderColor: '#10b98130',
    backgroundColor: '#10b98108',
  },
  missingBadge: {
    borderColor: '#ef444430',
    backgroundColor: '#ef444408',
    opacity: 0.7,
  },
  missingDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#ef4444',
  },
  upskillCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginTop: 20,
    padding: 16,
    backgroundColor: '#f59e0b08',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#f59e0b20',
  },
  upskillText: {
    color: '#fbbf24',
    fontSize: 12,
    fontWeight: '500',
    flex: 1,
  },
  footer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#0a0a0a',
    padding: 24,
    paddingBottom: Platform.OS === 'ios' ? 40 : 24,
    borderTopWidth: 1,
    borderTopColor: '#171717',
  },
  applyButton: {
    backgroundColor: '#7c3aed',
    height: 60,
    borderRadius: 18,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    shadowColor: '#7c3aed',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  applyButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  }
});
