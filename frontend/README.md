# AI SchoolOS Frontend

A unified web application for AI SchoolOS built with Next.js, TypeScript, and TailwindCSS.

## Features

- **Unified Web Application**: Single codebase for all user types (Admin, Teacher, Student, Parent)
- **Modern UI/UX**: Built with TailwindCSS and Framer Motion
- **Type Safety**: Full TypeScript support
- **State Management**: Redux Toolkit for global state
- **Data Fetching**: React Query for server state
- **Responsive Design**: Mobile-first approach
- **AI Integration**: Ready for AI-powered features

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **State Management**: Redux Toolkit
- **Data Fetching**: React Query
- **UI Components**: Headless UI, Lucide React
- **Animations**: Framer Motion
- **Forms**: React Hook Form

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Environment Variables

Create a `.env.local` file in the root directory:

```env
API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── admin/             # School Admin Dashboard
│   ├── teacher/           # Teacher Portal
│   ├── student/           # Student Portal
│   ├── parent/            # Parent Portal
│   ├── login/             # Authentication pages
│   └── register/
├── components/            # Reusable UI components
│   ├── ui/               # Basic UI components
│   ├── forms/            # Form components
│   └── layout/           # Layout components
├── store/                # Redux store and slices
├── hooks/                # Custom React hooks
├── utils/                # Utility functions
├── types/                # TypeScript type definitions
└── styles/               # Global styles
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## User Portals

### School Admin Dashboard (`/admin`)
- Complete school management
- Student and teacher management
- Fee management
- Attendance tracking
- AI insights and analytics
- Report generation

### Teacher Portal (`/teacher`)
- Class management
- Grade management
- Assignment creation
- Student progress tracking
- Communication tools

### Student Portal (`/student`)
- Course materials
- Assignment submission
- Grade viewing
- Attendance tracking
- Communication with teachers

### Parent Portal (`/parent`)
- Child progress monitoring
- Fee payment
- Communication with school
- Attendance tracking
- Academic reports

## Development Guidelines

### Code Style
- Use TypeScript for all new code
- Follow ESLint and Prettier configurations
- Use TailwindCSS for styling
- Implement responsive design

### Component Structure
- Use functional components with hooks
- Implement proper TypeScript interfaces
- Use Redux for global state
- Use React Query for server state

### Testing
- Write unit tests for components
- Test user interactions
- Ensure accessibility compliance

## Deployment

### Production Build
```bash
npm run build
npm run start
```

### Docker Deployment
```bash
docker build -t ai-schoolos-frontend .
docker run -p 3000:3000 ai-schoolos-frontend
```

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test your changes thoroughly
4. Update documentation as needed

## License

This project is part of the AI SchoolOS system. 