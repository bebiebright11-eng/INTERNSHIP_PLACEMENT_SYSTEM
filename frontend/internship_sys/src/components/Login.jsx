import React, { useState } from 'react';
import { 
  Box, Button, FormControl, FormLabel, Input, 
  VStack, Heading, useToast, Container, Center, Text 
} from '@chakra-ui/react';
import API from '../api';

const Login = ({ onLoginSuccess }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const toast = useToast();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            // POST request to your Django Token endpoint
            const response = await API.post('accounts/login/', {
                username: username,
                password: password
            });

            // Save the Token locally so we don't lose it on refresh
            localStorage.setItem('token', response.data.token);

            toast({
                title: "Login Successful",
                status: "success",
                duration: 2000,
                isClosable: true,
            });

            // Trigger the function in App.js to swap screens
            onLoginSuccess(); 
        } catch (error) {
            toast({
                title: "Login Failed",
                description: "Please check your credentials.",
                status: "error",
                duration: 3000,
                isClosable: true,
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Center h="100vh" bg="gray.100">
            <Container maxW="md" bg="white" p={10} borderRadius="2xl" boxShadow="xl">
                <form onSubmit={handleLogin}>
                    <VStack spacing={5}>
                        <Heading size="lg" color="blue.500">Student Portal</Heading>
                        <Text color="gray.500">Sign in to manage your placement</Text>
                        
                        <FormControl isRequired>
                            <FormLabel>Username (Reg No)</FormLabel>
                            <Input 
                                placeholder="e.g. 21/U/1234" 
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </FormControl>

                        <FormControl isRequired>
                            <FormLabel>Password</FormLabel>
                            <Input 
                                type="password" 
                                placeholder="********" 
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </FormControl>

                        <Button 
                            type="submit" 
                            colorScheme="blue" 
                            width="full" 
                            size="lg"
                            isLoading={loading}
                        >
                            Sign In
                        </Button>
                    </VStack>
                </form>
            </Container>
        </Center>
    );
};

export default Login;