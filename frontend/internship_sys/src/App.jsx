import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Button, Flex, Spacer, Heading } from '@chakra-ui/react';
import Login from './components/Login';
import StudentDashboard from './components/StudentDashboard';

function App() {
  // Logic: Check if token exists in browser memory on first load
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <ChakraProvider>
      <Box minH="100vh" bg="gray.50">
        {/* Simple Navigation Bar (Only shows when logged in) */}
        {isAuthenticated && (
          <Flex bg="blue.600" p={4} color="white" align="center" shadow="md">
            <Heading size="md">Internship System</Heading>
            <Spacer />
            <Button colorScheme="whiteAlpha" onClick={handleLogout}>
              Logout
            </Button>
          </Flex>
        )}

        {/* The Conditional Screen Switch */}
        {isAuthenticated ? (
          <StudentDashboard />
        ) : (
          <Login onLoginSuccess={handleLoginSuccess} />
        )}
      </Box>
    </ChakraProvider>
  );
}

export default App;