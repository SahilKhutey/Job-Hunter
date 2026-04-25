import React, { useEffect, useState } from 'react';
import { 
  StyleSheet, View, Text, FlatList, TouchableOpacity, 
  TextInput, ActivityIndicator, RefreshControl 
} from 'react-native';
import api from '../lib/api';
import { Search, Filter, Briefcase, ChevronRight, Zap } from 'lucide-react-native';

function JobItem({ job, onPress }) {
  const matchScore = Math.round(job.match_score * 100);
  const matchColor = matchScore > 80 ? '#10b981' : matchScore > 60 ? '#f59e0b' : '#6b7280';

  return (
    <TouchableOpacity style={styles.jobItem} onPress={onPress}>
      <View style={styles.jobHeader}>
        <View style={styles.companyIcon}>
          <Briefcase color="#a78bfa" size={20} />
        </View>
        <View style={styles.jobInfo}>
          <Text style={styles.jobTitle} numberOfLines={1}>{job.title}</Text>
          <Text style={styles.jobCompany}>{job.company}</Text>
        </View>
        <View style={[styles.matchBadge, { backgroundColor: matchColor + '15' }]}>
          <Zap color={matchColor} size={10} />
          <Text style={[styles.matchText, { color: matchColor }]}>{matchScore}%</Text>
        </View>
      </View>
      <View style={styles.jobFooter}>
        <Text style={styles.jobLocation}>{job.location}</Text>
        <ChevronRight color="#404040" size={18} />
      </View>
    </TouchableOpacity>
  );
}

export default function JobFeedScreen({ navigation }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch] = useState('');

  const fetchJobs = async () => {
    try {
      const res = await api.get('/jobs');
      setJobs(res.data);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchJobs().finally(() => setRefreshing(false));
  };

  const filteredJobs = jobs.filter(j => 
    j.title.toLowerCase().includes(search.toLowerCase()) || 
    j.company.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Intelligence Feed</Text>
        <TouchableOpacity style={styles.filterButton}>
          <Filter color="#fff" size={20} />
        </TouchableOpacity>
      </View>

      <View style={styles.searchContainer}>
        <Search color="#525252" size={18} style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search jobs..."
          placeholderTextColor="#525252"
          value={search}
          onChangeText={setSearch}
        />
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator color="#7c3aed" />
        </View>
      ) : (
        <FlatList
          data={filteredJobs}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <JobItem 
              job={item} 
              onPress={() => navigation.navigate('JobDetail', { job: item })} 
            />
          )}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#7c3aed" />
          }
          ListEmptyComponent={
            <View style={styles.empty}>
              <Text style={styles.emptyText}>No job intelligence found.</Text>
            </View>
          }
        />
      )}
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
    marginBottom: 20,
  },
  title: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  filterButton: {
    width: 40,
    height: 40,
    borderRadius: 12,
    backgroundColor: '#171717',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#262626',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#171717',
    marginHorizontal: 20,
    borderRadius: 16,
    paddingHorizontal: 16,
    height: 52,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#262626',
  },
  searchIcon: {
    marginRight: 12,
  },
  searchInput: {
    flex: 1,
    color: '#fff',
    fontSize: 16,
  },
  listContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  jobItem: {
    backgroundColor: '#171717',
    borderRadius: 20,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#262626',
  },
  jobHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  companyIcon: {
    width: 40,
    height: 40,
    borderRadius: 10,
    backgroundColor: '#7c3aed15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  jobInfo: {
    flex: 1,
  },
  jobTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  jobCompany: {
    color: '#737373',
    fontSize: 13,
    marginTop: 2,
  },
  matchBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    gap: 4,
  },
  matchText: {
    fontSize: 10,
    fontWeight: 'bold',
  },
  jobFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#262626',
    paddingTop: 12,
  },
  jobLocation: {
    color: '#525252',
    fontSize: 12,
  },
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  empty: {
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 60,
  },
  emptyText: {
    color: '#525252',
    fontSize: 14,
  }
});
