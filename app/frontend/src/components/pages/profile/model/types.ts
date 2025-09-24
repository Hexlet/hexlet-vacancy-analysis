export interface User {
  name: string;
  lastName: string;
  email: string;
  // phoneNumber: string,
  subscriptions: {
    isPro: boolean;
    validTill: string;
  },
  notifications: {
    newFilteredVacancies: boolean;
    weeklyAnalytics: boolean;
    newsAndUpdates: boolean;
  }
}

export type FormValues = {
  name: string;
  lastName: string;
  email: string;
  // phoneNumber: string;
}