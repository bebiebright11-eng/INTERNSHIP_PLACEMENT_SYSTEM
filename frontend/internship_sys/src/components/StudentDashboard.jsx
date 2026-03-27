import React, { useEffect, useState } from 'react';
import { 
  Box, Heading, Text, Stack, Button, 
  Divider, Alert, AlertIcon, Spinner, Center, Container, SimpleGrid, Stat, StatLabel, StatNumber
} from '@chakra-ui/react';
import API from '../api';

const StudentDashboard = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Calling your Django 'UserProfileView'
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

    if (loading) return <Center h="80vh"><Spinner size="xl" color="blue.500" /></Center>;

    if (!profile) return <Center h="80vh"><Text>Error loading profile. Please log in again.</Text></Center>;

    // Shortcut for the nested data we built in Django
    const studentData = profile.student_profile;

    return (
        <Container maxW="container.lg" py={10}>
            <Stack spacing={8}>
                {/* 1. Welcome Header */}
                <Box>
                    <Heading size="xl">Welcome, {profile.first_name}!</Heading>
                    <Text color="gray.600" fontSize="lg">Manage your internship placement and status here.</Text>
                </Box>

                {/* 2. Quick Stats Grid */}
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={5}>
                    <Box p={5} shadow="base" borderWidth="1px" borderRadius="md" bg="white">
                        <Stat>
                            <StatLabel color="gray.500">Registration Number</StatLabel>
                            <StatNumber fontSize="lg">{studentData.registration_number}</StatNumber>
                        </Stat>
                    </Box>
                    <Box p={5} shadow="base" borderWidth="1px" borderRadius="md" bg="white">
                        <Stat>
                            <StatLabel color="gray.500">Course</StatLabel>
                            <StatNumber fontSize="lg">{studentData.course}</StatNumber>
                        </Stat>
                    </Box>
                    <Box p={5} shadow="base" borderWidth="1px" borderRadius="md" bg="white">
                        <Stat>
                            <StatLabel color="gray.500">Year of Study</StatLabel>
                            <StatNumber fontSize="lg">Year {studentData.year_of_study}</StatNumber>
                        </Stat>
                    </Box>
                </SimpleGrid>

                {/* 3. Eligibility Status Area */}
                <Box p={8} borderWidth="1px" borderRadius="xl" bg="white" shadow="sm">
                    <Heading size="md" mb={4}>Placement Eligibility</Heading>
                    
                    {studentData.is_eligible ? (
                        <Stack spacing={4}>
                            <Alert status="success" variant="left-accent">
                                <AlertIcon />
                                You are officially eligible for internship placement!
                            </Alert>
                            <Button colorScheme="blue" size="lg" w="full">
                                Find a Placement Now
                            </Button>
                        </Stack>
                    ) : (
                        <Stack spacing={4}>
                            <Alert status="warning" variant="left-accent">
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