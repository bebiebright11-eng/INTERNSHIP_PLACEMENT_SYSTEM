import React, { useState } from 'react';
import {
  Box,
  Flex,
  Stack,
  Heading,
  Text,
  FormControl,
  FormLabel,
  Input,
  Button,
  useToast,
  InputGroup,
  InputRightElement,
  IconButton,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const toast = useToast();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Replace with your actual Django endpoint (e.g., /api/token/ or /api/login/)
      const response = await axios.post('http://127.0.0.1:8000/api/login/', {
        username,
        password,
      });

      // Save the token (Assuming JWT or Token Auth)
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user_role', response.data.role);

      toast({
        title: 'Login Successful',
        description: `Welcome back, ${username}!`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });

      // Redirect to student dashboard
      navigate('/dashboard');
    } catch (error) {
      toast({
        title: 'Login Failed',
        description: error.response?.data?.detail || 'Invalid credentials',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Flex minH={'100vh'} align={'center'} justify={'center'} bg={'gray.50'}>
      <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
        <Stack align={'center'}>
          <Heading fontSize={'4xl'}>Student Portal</Heading>
          <Text fontSize={'lg'} color={'gray.600'}>
            Sign in to manage your internship 🚀
          </Text>
        </Stack>
        <Box rounded={'lg'} bg={'white'} boxShadow={'lg'} p={8} minW={{ base: '90vw', md: '400px' }}>
          <form onSubmit={handleLogin}>
            <Stack spacing={4}>
              <FormControl id="username" isRequired>
                <FormLabel>Username</FormLabel>
                <Input 
                  type="text" 
                  value={username} 
                  onChange={(e) => setUsername(e.target.value)} 
                />
              </FormControl>
              <FormControl id="password" isRequired>
                <FormLabel>Password</FormLabel>
                <InputGroup>
                  <Input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <InputRightElement h={'full'}>
                    <IconButton
                      variant={'ghost'}
                      icon={showPassword ? <ViewOffIcon /> : <ViewIcon />}
                      onClick={() => setShowPassword((show) => !show)}
                    />
                  </InputRightElement>
                </InputGroup>
              </FormControl>
              <Stack spacing={10}>
                <Button
                  type="submit"
                  bg={'blue.400'}
                  color={'white'}
                  _hover={{ bg: 'blue.500' }}
                  isLoading={isLoading}
                >
                  Sign in
                </Button>
              </Stack>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Flex>
  );
};

export default Login;