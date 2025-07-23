'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Users, 
  GraduationCap, 
  Calendar, 
  BookOpen, 
  DollarSign, 
  BarChart3, 
  Settings, 
  Bell,
  Search,
  Plus,
  Filter,
  FileText,
  Clock,
  MapPin,
  Truck,
  MessageSquare,
  TrendingUp,
  ArrowRight,
  CheckCircle,
  Brain,
  Zap,
  Shield,
  Globe,
  Smartphone,
  Database,
  Cloud,
  Lock,
  Star,
  Play,
  ChevronRight,
  ChevronDown,
  Sparkles
} from 'lucide-react';

export default function HomePage() {
  const [activeTab, setActiveTab] = useState('features');

  const features = [
    {
      title: 'AI-Powered Analytics',
      description: 'Intelligent insights and predictive analytics for better decision making',
      icon: Brain,
      color: 'from-purple-500 to-pink-500',
      benefits: ['Predictive performance analysis', 'Smart attendance patterns', 'Automated grade predictions']
    },
    {
      title: 'Real-time Communication',
      description: 'Instant messaging and notifications across all stakeholders',
      icon: MessageSquare,
      color: 'from-blue-500 to-cyan-500',
      benefits: ['Instant parent notifications', 'Teacher-student messaging', 'Emergency alerts']
    },
    {
      title: 'Smart Attendance',
      description: 'Automated attendance tracking with facial recognition',
      icon: Clock,
      color: 'from-green-500 to-emerald-500',
      benefits: ['Facial recognition', 'GPS tracking', 'Automated reports']
    },
    {
      title: 'Intelligent Scheduling',
      description: 'AI-optimized timetables and resource allocation',
      icon: Calendar,
      color: 'from-orange-500 to-red-500',
      benefits: ['Conflict-free scheduling', 'Resource optimization', 'Dynamic adjustments']
    },
    {
      title: 'Advanced Security',
      description: 'Enterprise-grade security with role-based access control',
      icon: Shield,
      color: 'from-indigo-500 to-purple-500',
      benefits: ['Multi-factor authentication', 'Data encryption', 'Audit trails']
    },
    {
      title: 'Cloud-Native Architecture',
      description: 'Scalable microservices built for the modern cloud',
      icon: Cloud,
      color: 'from-teal-500 to-blue-500',
      benefits: ['99.9% uptime', 'Global CDN', 'Auto-scaling']
    }
  ];

  const stats = [
    { number: '500+', label: 'Schools Trust Us', icon: Users },
    { number: '50K+', label: 'Students Managed', icon: GraduationCap },
    { number: '99.9%', label: 'Uptime Guarantee', icon: Shield },
    { number: '24/7', label: 'Support Available', icon: MessageSquare }
  ];

  const testimonials = [
    {
      name: 'Dr. Sarah Johnson',
      role: 'Principal, St. Mary\'s School',
      content: 'AI SchoolOS transformed our school management. The AI-powered insights help us make data-driven decisions.',
      rating: 5
    },
    {
      name: 'Mr. David Chen',
      role: 'IT Director, Global Academy',
      content: 'The microservices architecture ensures our system is always available and scales perfectly with our growth.',
      rating: 5
    },
    {
      name: 'Mrs. Emily Davis',
      role: 'Administrator, Future School',
      content: 'Real-time communication features have improved parent engagement by 300%. Highly recommended!',
      rating: 5
    }
  ];

  const quickActions = [
    { title: 'Admin Portal', href: '/admin', color: 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800' },
    { title: 'Teacher Portal', href: '/teacher', color: 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800' },
    { title: 'Student Portal', href: '/student', color: 'bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800' },
    { title: 'Parent Portal', href: '/parent', color: 'bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-700 hover:to-orange-800' },
    { title: 'Super Admin', href: '/super-admin', color: 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI SchoolOS
                </h1>
                <p className="text-xs text-gray-500">Next-Gen School Management</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                href="/login" 
                className="text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Login
              </Link>
              <Link 
                href="#demo" 
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg text-sm font-medium hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                Try Demo
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Floating Elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-4 h-4 bg-blue-400 rounded-full animate-ping"></div>
          <div className="absolute top-40 right-20 w-3 h-3 bg-purple-400 rounded-full animate-ping animation-delay-1000"></div>
          <div className="absolute bottom-40 left-1/4 w-2 h-2 bg-pink-400 rounded-full animate-ping animation-delay-2000"></div>
          <div className="absolute top-1/2 right-1/3 w-5 h-5 bg-yellow-400 rounded-full animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-3 h-3 bg-green-400 rounded-full animate-bounce"></div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="inline-flex items-center space-x-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-6 animate-fade-in">
              <Sparkles className="h-4 w-4 animate-spin" />
              <span>AI-Powered School Management</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Transform Your School with
              <span className="block bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-gradient">
                AI Intelligence
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto leading-relaxed animate-fade-in-up">
              The world's most advanced school management platform powered by artificial intelligence. 
              Streamline operations, enhance communication, and drive student success with cutting-edge technology.
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6 mb-12">
              <Link 
                href="#demo"
                className="group bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-xl hover:shadow-2xl transform hover:-translate-y-1 hover:scale-105"
              >
                Start Free Trial
                <ArrowRight className="inline ml-2 h-5 w-5 group-hover:translate-x-2 transition-transform duration-300" />
              </Link>
              <button className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors group">
                <div className="relative">
                  <Play className="h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
                  <div className="absolute inset-0 bg-blue-500 rounded-full opacity-20 animate-ping"></div>
                </div>
                <span>Watch Demo</span>
              </button>
            </div>

            {/* Quick Access Portals with Hover Effects */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 max-w-4xl mx-auto">
              {quickActions.map((action, index) => (
                <Link
                  key={action.title}
                  href={action.href}
                  className={`${action.color} text-white p-4 rounded-xl text-center transition-all duration-300 hover:shadow-lg hover:-translate-y-2 hover:scale-105 transform`}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="text-sm font-medium">{action.title}</div>
                </Link>
              ))}
            </div>
          </div>
        </div>
        
        {/* Background Elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
          <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
          <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-yellow-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-1000"></div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center group">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mb-4 group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 relative">
                  <stat.icon className="h-8 w-8 text-white group-hover:animate-bounce" />
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full opacity-20 animate-ping"></div>
                </div>
                <div className="text-3xl md:text-4xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors duration-300">{stat.number}</div>
                <div className="text-gray-600 group-hover:text-gray-700 transition-colors duration-300">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Why Choose AI SchoolOS?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built with cutting-edge AI technology and microservices architecture for the modern educational institution.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-4 relative overflow-hidden">
                {/* Floating background elements */}
                <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
                <div className="absolute bottom-0 left-0 w-16 h-16 bg-gradient-to-br from-pink-100 to-yellow-100 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500 delay-100"></div>
                
                <div className={`inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 relative z-10`}>
                  <feature.icon className="h-8 w-8 text-white group-hover:animate-pulse" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors duration-300">{feature.title}</h3>
                <p className="text-gray-600 mb-6 leading-relaxed group-hover:text-gray-700 transition-colors duration-300">{feature.description}</p>
                <ul className="space-y-3">
                  {feature.benefits.map((benefit, idx) => (
                    <li key={idx} className="flex items-center space-x-3 group/item">
                      <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 group-hover/item:scale-110 transition-transform duration-200" />
                      <span className="text-gray-700 group-hover/item:text-gray-900 transition-colors duration-200">{benefit}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Trusted by Leading Schools
            </h2>
            <p className="text-xl text-gray-600">
              See what educators are saying about AI SchoolOS
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all duration-500 hover:-translate-y-2 group relative overflow-hidden">
                {/* Floating background elements */}
                <div className="absolute top-0 right-0 w-16 h-16 bg-gradient-to-br from-blue-200 to-purple-200 rounded-full opacity-30 group-hover:scale-150 transition-transform duration-500"></div>
                
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current group-hover:scale-110 transition-transform duration-200" style={{ animationDelay: `${i * 100}ms` }} />
                  ))}
                </div>
                <p className="text-gray-700 mb-6 leading-relaxed group-hover:text-gray-800 transition-colors duration-300">"{testimonial.content}"</p>
                <div className="group-hover:translate-x-2 transition-transform duration-300">
                  <div className="font-semibold text-gray-900">{testimonial.name}</div>
                  <div className="text-gray-600">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Transform Your School?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            Join hundreds of schools already using AI SchoolOS to streamline their operations and enhance student success.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
            <Link 
              href="/login"
              className="bg-white text-blue-600 px-8 py-4 rounded-xl text-lg font-semibold hover:bg-gray-50 transition-all duration-200 shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
            >
              Start Free Trial
            </Link>
            <Link 
              href="#contact"
              className="text-white border-2 border-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-white hover:text-blue-600 transition-all duration-200"
            >
              Contact Sales
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Sparkles className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold">AI SchoolOS</span>
              </div>
              <p className="text-gray-400">
                The future of school management powered by artificial intelligence.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#" className="hover:text-white transition-colors">Features</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Security</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">API</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Blog</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Careers</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Documentation</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Status</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 AI SchoolOS. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
} 