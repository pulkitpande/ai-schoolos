'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard,
  Users,
  GraduationCap,
  DollarSign,
  BookOpen,
  Calendar,
  UserCheck,
  FileText,
  Library,
  Bus,
  MessageSquare,
  BarChart3,
  Bell,
  Settings,
  LogOut,
  ChevronDown,
  School,
  BookMarked,
  Clock,
  MapPin,
  Phone,
  Mail,
  User,
  Shield,
  Database,
  Activity
} from 'lucide-react';
import { useAuthStatus } from '../hooks/useApi';

interface NavigationProps {
  className?: string;
}

interface MenuItem {
  title: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  roles: string[];
  children?: MenuItem[];
}

// Utility function to replace cn
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

const menuItems: MenuItem[] = [
  {
    title: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
    roles: ['admin', 'teacher', 'student', 'parent', 'super_admin'],
  },
  {
    title: 'Academic',
    href: '/academic',
    icon: School,
    roles: ['admin', 'teacher', 'student', 'parent'],
    children: [
      {
        title: 'Students',
        href: '/academic/students',
        icon: Users,
        roles: ['admin', 'teacher'],
      },
      {
        title: 'Staff',
        href: '/academic/staff',
        icon: GraduationCap,
        roles: ['admin'],
      },
      {
        title: 'Exams',
        href: '/academic/exams',
        icon: BookOpen,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'Homework',
        href: '/academic/homework',
        icon: FileText,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'Timetable',
        href: '/academic/timetable',
        icon: Clock,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
    ],
  },
  {
    title: 'Financial',
    href: '/financial',
    icon: DollarSign,
    roles: ['admin', 'parent'],
    children: [
      {
        title: 'Fee Management',
        href: '/financial/fees',
        icon: DollarSign,
        roles: ['admin'],
      },
      {
        title: 'Payments',
        href: '/financial/payments',
        icon: DollarSign,
        roles: ['admin', 'parent'],
      },
      {
        title: 'Reports',
        href: '/financial/reports',
        icon: BarChart3,
        roles: ['admin'],
      },
    ],
  },
  {
    title: 'Attendance',
    href: '/attendance',
    icon: UserCheck,
    roles: ['admin', 'teacher', 'student', 'parent'],
    children: [
      {
        title: 'Mark Attendance',
        href: '/attendance/mark',
        icon: UserCheck,
        roles: ['admin', 'teacher'],
      },
      {
        title: 'View Records',
        href: '/attendance/records',
        icon: Calendar,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'Reports',
        href: '/attendance/reports',
        icon: BarChart3,
        roles: ['admin', 'teacher'],
      },
    ],
  },
  {
    title: 'Library',
    href: '/library',
    icon: Library,
    roles: ['admin', 'teacher', 'student', 'parent'],
    children: [
      {
        title: 'Books',
        href: '/library/books',
        icon: BookMarked,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'Borrowings',
        href: '/library/borrowings',
        icon: Library,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'Members',
        href: '/library/members',
        icon: Users,
        roles: ['admin'],
      },
    ],
  },
  {
    title: 'Transport',
    href: '/transport',
    icon: Bus,
    roles: ['admin', 'student', 'parent'],
    children: [
      {
        title: 'Vehicles',
        href: '/transport/vehicles',
        icon: Bus,
        roles: ['admin'],
      },
      {
        title: 'Routes',
        href: '/transport/routes',
        icon: MapPin,
        roles: ['admin'],
      },
      {
        title: 'Bookings',
        href: '/transport/bookings',
        icon: Calendar,
        roles: ['admin', 'student', 'parent'],
      },
      {
        title: 'Drivers',
        href: '/transport/drivers',
        icon: Users,
        roles: ['admin'],
      },
    ],
  },
  {
    title: 'Communication',
    href: '/communication',
    icon: MessageSquare,
    roles: ['admin', 'teacher', 'student', 'parent'],
    children: [
      {
        title: 'Messages',
        href: '/communication/messages',
        icon: MessageSquare,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'Announcements',
        href: '/communication/announcements',
        icon: Bell,
        roles: ['admin', 'teacher'],
      },
      {
        title: 'Notifications',
        href: '/communication/notifications',
        icon: Bell,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
    ],
  },
  {
    title: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
    roles: ['admin', 'teacher'],
    children: [
      {
        title: 'Dashboard',
        href: '/analytics/dashboard',
        icon: BarChart3,
        roles: ['admin', 'teacher'],
      },
      {
        title: 'Reports',
        href: '/analytics/reports',
        icon: FileText,
        roles: ['admin', 'teacher'],
      },
      {
        title: 'Metrics',
        href: '/analytics/metrics',
        icon: Activity,
        roles: ['admin', 'teacher'],
      },
    ],
  },
  {
    title: 'Settings',
    href: '/settings',
    icon: Settings,
    roles: ['admin', 'teacher', 'student', 'parent'],
    children: [
      {
        title: 'Profile',
        href: '/settings/profile',
        icon: User,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'Security',
        href: '/settings/security',
        icon: Shield,
        roles: ['admin', 'teacher', 'student', 'parent'],
      },
      {
        title: 'System',
        href: '/settings/system',
        icon: Database,
        roles: ['admin'],
      },
    ],
  },
];

export default function Navigation({ className }: NavigationProps) {
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());
  const pathname = usePathname();
  const authStatus = useAuthStatus();

  const toggleExpanded = (href: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(href)) {
      newExpanded.delete(href);
    } else {
      newExpanded.add(href);
    }
    setExpandedItems(newExpanded);
  };

  const isActive = (href: string) => {
    return pathname === href || pathname.startsWith(href + '/');
  };

  const hasAccess = (roles: string[]) => {
    if (!authStatus?.storedUser) return false;
    return roles.includes(authStatus.storedUser.role);
  };

  const renderMenuItem = (item: MenuItem) => {
    if (!hasAccess(item.roles)) return null;

    const isExpanded = expandedItems.has(item.href);
    const hasChildren = item.children && item.children.length > 0;
    const isActiveItem = isActive(item.href);

    return (
      <div key={item.href}>
        <Link
          href={item.href}
          className={cn(
            'flex items-center justify-between px-3 py-2 text-sm font-medium rounded-md transition-colors',
            isActiveItem
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          )}
          onClick={() => {
            if (hasChildren) {
              toggleExpanded(item.href);
            }
          }}
        >
          <div className="flex items-center">
            <item.icon className="h-4 w-4 mr-3" />
            <span>{item.title}</span>
          </div>
          {hasChildren && (
            <ChevronDown
              className={cn(
                'h-4 w-4 transition-transform',
                isExpanded ? 'rotate-180' : ''
              )}
            />
          )}
        </Link>
        
        {hasChildren && isExpanded && (
          <div className="ml-4 mt-1 space-y-1">
            {item.children!.map((child) => {
              if (!hasAccess(child.roles)) return null;
              
              const isActiveChild = isActive(child.href);
              
              return (
                <Link
                  key={child.href}
                  href={child.href}
                  className={cn(
                    'flex items-center px-3 py-2 text-sm rounded-md transition-colors',
                    isActiveChild
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                  )}
                >
                  <child.icon className="h-4 w-4 mr-3" />
                  <span>{child.title}</span>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  return (
    <nav className={cn('space-y-1', className)}>
      {menuItems.map(renderMenuItem)}
    </nav>
  );
} 