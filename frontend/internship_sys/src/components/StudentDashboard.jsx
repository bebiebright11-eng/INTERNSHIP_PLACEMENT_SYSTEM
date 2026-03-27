import React, { useEffect, useState } from 'react';
import { 
  Box, Heading, Text, Stack, Button, Divider, Alert, AlertIcon, 
  Spinner, Center, Container, Table, Thead, Tbody, Tr, Th, Td, 
  TableContainer, Badge, Flex
} from '@chakra-ui/react';
import API from '../api';

const StudentDashboard = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        API.get('accounts/profile/')
            .then(res => {
                setProfile(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Error fetching profile", err);
                setLoading(false);
            });
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/';
    };

    if (loading) return <Center h="80vh"><Spinner size="xl" color="blue.500" /></Center>;
    if (!profile) return <Center h="80vh"><Text>Error loading profile. Please log in again.</Text></Center>;

    // Matching your serializer: profile.profile contains student_profile data
    const studentData = profile.profile;

    return (
        <Container maxW="container.lg" py={10}>
            <Stack spacing={8}>
                
                {/* 1. Header with Name and Logout */}
                <Flex justifyContent="space-between" alignItems="center" bg="white" p={6} borderRadius="lg" shadow="sm" borderWidth="1px">
                    <Box>
                        <Heading size="lg" color="blue.800">
                            Welcome, {profile?.first_name || "Student"}!
                        </Heading>
                        <Text color="gray.600">Internship Placement System Portal</Text>
                    </Box>
                    <Button colorScheme="red" variant="outline" size="sm" onClick={handleLogout}>
                        Logout
                    </Button>
                </Flex>

                {/* 2. Academic Information Table */}
                <Box bg="white" p={6} borderRadius="xl" shadow="md" borderWidth="1px">
                    <Heading size="md" mb={4} color="gray.700">Academic Details</Heading>
                    <TableContainer>
                        <Table variant="simple">
                            <Thead bg="gray.50">
                                <Tr>
                                    <Th>Information Field</Th>
                                    <Th>Details</Th>
                                    <Th>Status</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                <Tr>
                                    <Td fontWeight="bold">Registration Number</Td>
                                    <Td>{studentData?.registration_number}</Td>
                                    <Td><Badge colorScheme="blue">Verified</Badge></Td>
                                </Tr>
                                <Tr>
                                    <Td fontWeight="bold">Course</Td>
                                    <Td textTransform="capitalize">{studentData?.course}</Td>
                                    <Td><Badge colorScheme="green">Enrolled</Badge></Td>
                                </Tr>
                                <Tr>
                                    <Td fontWeight="bold">Year of Study</Td>
                                    <Td>Year {studentData?.year_of_study}</Td>
                                    <Td><Badge colorScheme="purple">Active</Badge></Td>
                                </Tr>
                            </Tbody>
                        </Table>
                    </TableContainer>
                </Box>

                {/* 3. Eligibility Status Area */}
                <Box p={8} borderWidth="1px" borderRadius="xl" bg="white" shadow="sm" borderTop="4px solid" borderColor={studentData?.is_eligible ? "green.400" : "orange.400"}>
                    <Heading size="md" mb={4}>Placement Eligibility</Heading>
                    
                    {studentData?.is_eligible ? (
                        <Stack spacing={4}>
                            <Alert status="success" variant="left-accent" borderRadius="md">
                                <AlertIcon />
                                You are officially eligible for internship placement!
                            </Alert>
                            <Button colorScheme="blue" size="lg" w="full" shadow="md">
                                Find a Placement Now
                            </Button>
                        </Stack>
                    ) : (
                        <Stack spacing={4}>
                            <Alert status="warning" variant="left-accent" borderRadius="md">
                                <AlertIcon />
                                Eligibility Pending: Please ensure your documents are verified by your supervisor.
                            </Alert>
                            <Button isDisabled size="lg" w="full">
                                Applications Closed (Ineligible)
                            </Button>
                        </Stack>
                    )}
                </Box>

                <Divider />
            </Stack>
        </Container>
    );
};

export default StudentDashboard;