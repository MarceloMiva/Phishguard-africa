// This file exports TypeScript interfaces and types used across the application for type safety.

export interface User {
    id: number;
    name: string;
    email: string;
}

export interface Product {
    id: number;
    name: string;
    price: number;
}

export type Response<T> = {
    success: boolean;
    data: T;
    message?: string;
};