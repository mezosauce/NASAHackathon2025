import React, { useState, useMemo } from 'react';
import { Search, FileText, TrendingUp, Users, Rocket, Moon, BookOpen, BarChart3, Filter, ChevronDown, ChevronUp, X } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, ScatterChart, Scatter, ZAxis } from 'recharts';
import Axios from 'axios';
// Mock data structure - in production, this would come from NASA repository
const generatePublications = () => {
    const BASE_URL = 'http://LOCALHOST:80/api/'; // Placeholder URL
    const topics = set();
    const organisms = set();
    const missions = set();
    const years = Array.from({ length: 25 }, (_, i) => 2000 + i);

    const publications = Axios.get(`${BASE_URL}/articles`).then(res => res.data);

    return Array.from(publications

    return Array.from({ length: 608 }, (_, i) => ({
        id: i + 1,
        title: `Impact of ${topics[Math.floor(Math.random() * topics.length)]} on ${organisms[Math.floor(Math.random() * organisms.length)]} in Space Environment`,
        authors: `Author ${i + 1} et al.`,
        year: years[Math.floor(Math.random() * years.length)],
        topic: topics[Math.floor(Math.random() * topics.length)],
        organism: organisms[Math.floor(Math.random() * organisms.length)],
        mission: missions[Math.floor(Math.random() * missions.length)],
        citations: Math.floor(Math.random() * 150),
        keyFindings: [
            'Significant changes observed in cellular response',
            'Novel adaptation mechanisms identified',
            'Potential countermeasures proposed'
        ],
        researchGap: Math.random() > 0.7,
        actionable: Math.random() > 0.5
    }));
};

const NASABioscienceDashboard = () => {
    const [publications] = useState(generatePublications());
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedTopic, setSelectedTopic] = useState('All');
    const [selectedOrganism, setSelectedOrganism] = useState('All');
    const [selectedView, setSelectedView] = useState('overview');
    const [showFilters, setShowFilters] = useState(false);
    const [selectedPublication, setSelectedPublication] = useState(null);

    // Extract unique values for filters
    const topics = ['All', ...new Set(publications.map(p => p.topic))];
    const organisms = ['All', ...new Set(publications.map(p => p.organism))];

    // Filter publications
    const filteredPublications = useMemo(() => {
        return publications.filter(pub => {
            const matchesSearch = pub.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                pub.authors.toLowerCase().includes(searchQuery.toLowerCase());
            const matchesTopic = selectedTopic === 'All' || pub.topic === selectedTopic;
            const matchesOrganism = selectedOrganism === 'All' || pub.organism === selectedOrganism;
            return matchesSearch && matchesTopic && matchesOrganism;
        });
    }, [publications, searchQuery, selectedTopic, selectedOrganism]);

    // Analytics data
    const topicDistribution = useMemo(() => {
        const counts = {};
        filteredPublications.forEach(pub => {
            counts[pub.topic] = (counts[pub.topic] || 0) + 1;
        });
        return Object.entries(counts).map(([name, value]) => ({ name, value }));
    }, [filteredPublications]);

    const yearDistribution = useMemo(() => {
        const counts = {};
        filteredPublications.forEach(pub => {
            counts[pub.year] = (counts[pub.year] || 0) + 1;
        });
        return Object.entries(counts)
            .map(([year, count]) => ({ year: parseInt(year), count }))
            .sort((a, b) => a.year - b.year);
    }, [filteredPublications]);

    const organismDistribution = useMemo(() => {
        const counts = {};
        filteredPublications.forEach(pub => {
            counts[pub.organism] = (counts[pub.organism] || 0) + 1;
        });
        return Object.entries(counts).map(([name, value]) => ({ name, value }));
    }, [filteredPublications]);

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658'];

    const stats = {
        total: filteredPublications.length,
        researchGaps: filteredPublications.filter(p => p.researchGap).length,
        actionable: filteredPublications.filter(p => p.actionable).length,
        avgCitations: Math.round(filteredPublications.reduce((sum, p) => sum + p.citations, 0) / filteredPublications.length)
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
            {/* Header */}
            <header className="bg-black bg-opacity-50 backdrop-blur-md border-b border-blue-500">
                <div className="container mx-auto px-4 py-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                            <Rocket className="w-10 h-10 text-blue-400" />
                            <div>
                                <h1 className="text-3xl font-bold text-white">NASA Bioscience Explorer</h1>
                                <p className="text-blue-300 text-sm">608 Publications | Space Biology Research Database</p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={() => setSelectedView('overview')}
                                className={`px-4 py-2 rounded-lg transition-all ${selectedView === 'overview' ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
                            >
                                <BarChart3 className="w-5 h-5 inline mr-2" />
                                Overview
                            </button>
                            <button
                                onClick={() => setSelectedView('explore')}
                                className={`px-4 py-2 rounded-lg transition-all ${selectedView === 'explore' ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
                            >
                                <Search className="w-5 h-5 inline mr-2" />
                                Explore
                            </button>
                        </div>
                    </div>

                    {/* Search and Filters */}
                    <div className="flex gap-3">
                        <div className="flex-1 relative">
                            <Search className="absolute left-3 top-3 w-5 h-5 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Search publications by title, author, keywords..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
                            />
                        </div>
                        <button
                            onClick={() => setShowFilters(!showFilters)}
                            className="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white hover:bg-slate-700 transition-all flex items-center gap-2"
                        >
                            <Filter className="w-5 h-5" />
                            Filters
                            {showFilters ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>
                    </div>

                    {/* Filter Panel */}
                    {showFilters && (
                        <div className="mt-4 p-4 bg-slate-800 rounded-lg border border-slate-700">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-300 mb-2">Research Topic</label>
                                    <select
                                        value={selectedTopic}
                                        onChange={(e) => setSelectedTopic(e.target.value)}
                                        className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                                    >
                                        {topics.map(topic => (
                                            <option key={topic} value={topic}>{topic}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-300 mb-2">Organism</label>
                                    <select
                                        value={selectedOrganism}
                                        onChange={(e) => setSelectedOrganism(e.target.value)}
                                        className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500"
                                    >
                                        {organisms.map(org => (
                                            <option key={org} value={org}>{org}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-8">
                {selectedView === 'overview' ? (
                    <>
                        {/* Stats Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                            <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg p-6 text-white">
                                <div className="flex items-center justify-between mb-2">
                                    <FileText className="w-8 h-8 opacity-80" />
                                    <span className="text-3xl font-bold">{stats.total}</span>
                                </div>
                                <p className="text-blue-100">Total Publications</p>
                            </div>
                            <div className="bg-gradient-to-br from-orange-600 to-orange-800 rounded-lg p-6 text-white">
                                <div className="flex items-center justify-between mb-2">
                                    <TrendingUp className="w-8 h-8 opacity-80" />
                                    <span className="text-3xl font-bold">{stats.researchGaps}</span>
                                </div>
                                <p className="text-orange-100">Research Gaps Identified</p>
                            </div>
                            <div className="bg-gradient-to-br from-green-600 to-green-800 rounded-lg p-6 text-white">
                                <div className="flex items-center justify-between mb-2">
                                    <Rocket className="w-8 h-8 opacity-80" />
                                    <span className="text-3xl font-bold">{stats.actionable}</span>
                                </div>
                                <p className="text-green-100">Actionable Insights</p>
                            </div>
                            <div className="bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg p-6 text-white">
                                <div className="flex items-center justify-between mb-2">
                                    <BookOpen className="w-8 h-8 opacity-80" />
                                    <span className="text-3xl font-bold">{stats.avgCitations}</span>
                                </div>
                                <p className="text-purple-100">Avg. Citations</p>
                            </div>
                        </div>

                        {/* Charts */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                            {/* Publications Over Time */}
                            <div className="bg-slate-800 bg-opacity-50 backdrop-blur-md rounded-lg p-6 border border-slate-700">
                                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                    <TrendingUp className="w-5 h-5 text-blue-400" />
                                    Publications Over Time
                                </h3>
                                <ResponsiveContainer width="100%" height={250}>
                                    <LineChart data={yearDistribution}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                        <XAxis dataKey="year" stroke="#9CA3AF" />
                                        <YAxis stroke="#9CA3AF" />
                                        <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }} />
                                        <Line type="monotone" dataKey="count" stroke="#3B82F6" strokeWidth={2} dot={{ fill: '#3B82F6' }} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>

                            {/* Topic Distribution */}
                            <div className="bg-slate-800 bg-opacity-50 backdrop-blur-md rounded-lg p-6 border border-slate-700">
                                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                    <BarChart3 className="w-5 h-5 text-green-400" />
                                    Research Topics
                                </h3>
                                <ResponsiveContainer width="100%" height={250}>
                                    <BarChart data={topicDistribution.slice(0, 6)}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                        <XAxis dataKey="name" stroke="#9CA3AF" angle={-45} textAnchor="end" height={100} />
                                        <YAxis stroke="#9CA3AF" />
                                        <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }} />
                                        <Bar dataKey="value" fill="#10B981" />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>

                            {/* Organism Distribution */}
                            <div className="bg-slate-800 bg-opacity-50 backdrop-blur-md rounded-lg p-6 border border-slate-700">
                                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                    <Users className="w-5 h-5 text-purple-400" />
                                    Model Organisms
                                </h3>
                                <ResponsiveContainer width="100%" height={250}>
                                    <PieChart>
                                        <Pie
                                            data={organismDistribution}
                                            cx="50%"
                                            cy="50%"
                                            labelLine={false}
                                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                                            outerRadius={80}
                                            fill="#8884d8"
                                            dataKey="value"
                                        >
                                            {organismDistribution.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }} />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>

                            {/* Key Insights */}
                            <div className="bg-slate-800 bg-opacity-50 backdrop-blur-md rounded-lg p-6 border border-slate-700">
                                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                                    <Moon className="w-5 h-5 text-yellow-400" />
                                    Key Insights for Mission Planning
                                </h3>
                                <div className="space-y-3">
                                    <div className="p-3 bg-blue-900 bg-opacity-30 rounded-lg border-l-4 border-blue-500">
                                        <p className="text-white font-medium">Most Studied: Microgravity Effects</p>
                                        <p className="text-slate-300 text-sm">Critical for long-duration missions</p>
                                    </div>
                                    <div className="p-3 bg-orange-900 bg-opacity-30 rounded-lg border-l-4 border-orange-500">
                                        <p className="text-white font-medium">Research Gap: Mars-Specific Studies</p>
                                        <p className="text-slate-300 text-sm">Limited data on partial gravity effects</p>
                                    </div>
                                    <div className="p-3 bg-green-900 bg-opacity-30 rounded-lg border-l-4 border-green-500">
                                        <p className="text-white font-medium">Breakthrough: Cellular Adaptation</p>
                                        <p className="text-slate-300 text-sm">Novel countermeasures identified</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </>
                ) : (
                    /* Explore View - Publications List */
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <div className="lg:col-span-2 space-y-4">
                            <div className="bg-slate-800 bg-opacity-50 backdrop-blur-md rounded-lg p-4 border border-slate-700">
                                <h3 className="text-lg font-semibold text-white mb-2">
                                    Found {filteredPublications.length} publications
                                </h3>
                            </div>

                            <div className="space-y-3 max-h-[800px] overflow-y-auto pr-2">
                                {filteredPublications.slice(0, 50).map(pub => (
                                    <div
                                        key={pub.id}
                                        onClick={() => setSelectedPublication(pub)}
                                        className="bg-slate-800 bg-opacity-50 backdrop-blur-md rounded-lg p-4 border border-slate-700 hover:border-blue-500 transition-all cursor-pointer"
                                    >
                                        <div className="flex justify-between items-start mb-2">
                                            <h4 className="text-white font-semibold flex-1">{pub.title}</h4>
                                            {pub.actionable && (
                                                <span className="ml-2 px-2 py-1 bg-green-600 text-white text-xs rounded-full">Actionable</span>
                                            )}
                                        </div>
                                        <p className="text-slate-400 text-sm mb-2">{pub.authors} • {pub.year}</p>
                                        <div className="flex flex-wrap gap-2">
                                            <span className="px-2 py-1 bg-blue-600 text-white text-xs rounded">{pub.topic}</span>
                                            <span className="px-2 py-1 bg-purple-600 text-white text-xs rounded">{pub.organism}</span>
                                            <span className="px-2 py-1 bg-slate-700 text-slate-300 text-xs rounded">{pub.mission}</span>
                                            <span className="px-2 py-1 bg-orange-600 text-white text-xs rounded">{pub.citations} citations</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Publication Detail Panel */}
                        <div className="lg:col-span-1">
                            <div className="bg-slate-800 bg-opacity-50 backdrop-blur-md rounded-lg p-6 border border-slate-700 sticky top-4">
                                {selectedPublication ? (
                                    <>
                                        <div className="flex justify-between items-start mb-4">
                                            <h3 className="text-xl font-bold text-white">Publication Details</h3>
                                            <button
                                                onClick={() => setSelectedPublication(null)}
                                                className="text-slate-400 hover:text-white"
                                            >
                                                <X className="w-5 h-5" />
                                            </button>
                                        </div>
                                        <div className="space-y-4">
                                            <div>
                                                <h4 className="text-white font-semibold mb-2">{selectedPublication.title}</h4>
                                                <p className="text-slate-400 text-sm">{selectedPublication.authors}</p>
                                            </div>
                                            <div className="grid grid-cols-2 gap-3">
                                                <div className="bg-slate-900 p-3 rounded">
                                                    <p className="text-slate-400 text-xs">Year</p>
                                                    <p className="text-white font-semibold">{selectedPublication.year}</p>
                                                </div>
                                                <div className="bg-slate-900 p-3 rounded">
                                                    <p className="text-slate-400 text-xs">Citations</p>
                                                    <p className="text-white font-semibold">{selectedPublication.citations}</p>
                                                </div>
                                            </div>
                                            <div>
                                                <p className="text-slate-400 text-sm mb-2">Mission</p>
                                                <span className="px-3 py-1 bg-blue-600 text-white text-sm rounded">{selectedPublication.mission}</span>
                                            </div>
                                            <div>
                                                <p className="text-slate-400 text-sm mb-2">Key Findings</p>
                                                <ul className="space-y-2">
                                                    {selectedPublication.keyFindings.map((finding, idx) => (
                                                        <li key={idx} className="text-slate-300 text-sm flex items-start gap-2">
                                                            <span className="text-blue-400 mt-1">•</span>
                                                            <span>{finding}</span>
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                            {selectedPublication.researchGap && (
                                                <div className="p-3 bg-orange-900 bg-opacity-30 rounded border-l-4 border-orange-500">
                                                    <p className="text-orange-300 text-sm font-medium">⚠️ Research Gap Identified</p>
                                                    <p className="text-slate-300 text-xs mt-1">Additional studies recommended</p>
                                                </div>
                                            )}
                                        </div>
                                    </>
                                ) : (
                                    <div className="text-center py-12">
                                        <FileText className="w-16 h-16 text-slate-600 mx-auto mb-4" />
                                        <p className="text-slate-400">Select a publication to view details</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default NASABioscienceDashboard;