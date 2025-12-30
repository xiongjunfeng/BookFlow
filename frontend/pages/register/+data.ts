// https://vike.dev/data

import type { PageContextServer } from "vike/types";

export type Data = Awaited<ReturnType<typeof data>>;

export async function data(_pageContext: PageContextServer) {
  // Initialize empty form data for SSR
  const initialFormData = {
    username: '',
    password: '',
    confirmPassword: ''
  };
  return { initialFormData };
}