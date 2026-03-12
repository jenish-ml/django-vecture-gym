# Vecture Gym Management System - Implementation Plan

## Goal Description
Build a comprehensive Gym Management System named "Vecture" using Django, SQLite3, HTML, CSS, and JS. The system caters to three main user roles: Admin, Trainer, and Member (Online/Offline). It includes a public-facing website, a full e-commerce shop for members, fitness progressing tracking, and specialized dashboards with sidebar layouts for Admins and Trainers. 

## User Review Required
> [!IMPORTANT]
> The requested system is quite extensive. Please review the proposed app structure and database models below.
> The Member login specifies selecting "Login as Admin, Trainer, Member (online/offline)" which means the login form itself needs role selection. I will implement a unified login system that validates if the selected role matches the user's actual registered role. 

## Proposed Architecture

### Apps Structure
We will break the project down into manageable Django apps:
1. `accounts`: Handles Custom User Model, User Profiles, Registration, and Login logic.
2. `core`: Handles public-facing static-like content (Home, About, Contact).
3. `fitness`: Handles Gym Goals, Membership/Nutrition Plans, Workout/Diet allocations, and Progress tracking.
4. `shop`: E-commerce catalog, Cart, Orders, and Payments.
5. `dashboard`: Consolidated views for Admin, Trainer, and Member portals (leveraging shared sidebar templates).

### Database Models Overview

#### Accounts App
- **User (Custom AbstractUser)**
  - `role`: Choices (Admin, Trainer, Member)
  - `member_type`: Choices (Online, Offline, None)
  - `phone_no`: CharField
- **UserProfile**
  - OneToOne with `User`
  - `fitness_goal`: FK to GymGoal
  - `trainer`: FK to User (filtered by Trainer role)
  - `membership_plan`: FK to MembershipPlan
  - `nutrition_plan`: FK to NutritionPlan (Nullable for Online)

#### Fitness App
- **GymGoal**: `name`, `description`
- **MembershipPlan**: `name`, `price`, `duration_months`, `description`
- **NutritionPlan**: `name`, `description`
- **WorkoutPlan**: `trainer` (FK User), `member` (FK User), `week_start_date`, `day_1_plan` to `day_7_plan`.
- **DietPlan**: `trainer` (FK User), `member` (FK User), `duration_months` (Default 3), `detailed_plan`.
- **UserProgress**: `member` (FK User), `date`, `weight`, `notes` (Used for Chart.js).

#### Shop App
- **Product**: `name`, `description`, `price`, `image`, `is_active`
- **Order**: `member` (FK User), `total_amount`, `status` (Pending, Paid)
- **Payment**: Tracks Membership fees & Shop orders.

#### Core App
- **ContactMessage**: `name`, `email`, `message`, `is_resolved`

### Frontend Approach
- **Vanilla CSS & JS**: As requested, we will use plain HTML/CSS/JS without heavy frameworks like React.
- **Sidebars**: We will design a clean, responsive sidebar layout for the Admin and Trainer dashboards using CSS Flexbox/Grid.
- **Charts**: We will use Chart.js for the trainer to view member progress.
- **Carousel**: A pure CSS or minimal JS implementation for the home page carousel.

## Verification Plan
### Automated Tests
- Basic unit tests for custom user creation and role assignments.
### Manual Verification
1. Run local dev server (`python manage.py runserver`).
2. Navigate to public pages (Home, About, Trainers, Products) and test responsiveness.
3. Register a new user as Member (Online) and test purchasing flow.
4. Login as Admin, populate plans/goals/trainers, and verify Dashboard CRUD.
5. Login as Trainer, view assigned members, and create a workout/diet plan.
6. Verify offline member nutrition viewing logic.
