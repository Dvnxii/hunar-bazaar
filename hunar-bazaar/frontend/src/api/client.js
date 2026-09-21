// Axios instance with credentials so the HTTP-only JWT cookies set by the
// backend are sent automatically - no token handling in frontend state.
import axios from "axios";

export const api = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      // Session expired or not logged in - let the caller decide how to route.
    }
    return Promise.reject(err);
  }
);
