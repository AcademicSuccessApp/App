// Mock save result API
export async function saveResult(data) {
  // Simulate network delay
  await new Promise((res) => setTimeout(res, 500));
  // In a real app, send data to backend here
  return { success: true };
} 