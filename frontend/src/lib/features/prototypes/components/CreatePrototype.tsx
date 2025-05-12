import { authAxios } from "$lib/features/auth/state/auth";
import { createPrototypeAtom } from "$lib/features/prototypes/atoms";
import { useSystemDiagrams, useSystemInterfaces } from "$lib/features/prototypes/queries";
import {
    Button,
    CircularProgress,
    Divider,
    FormControl,
    FormLabel,
    Input,
    Modal,
    ModalClose,
    ModalDialog,
    Switch,
    Typography
} from "@mui/joy";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import CryptoJS from 'crypto-js';
import { useAtom } from "jotai";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import Select from "react-select";
 
type PrototypeInput = {
    name: string;
    description?: string;
    system: string;
    running?: boolean;
    metadata: Record<string, any>;
    database_hash?: string;
};
 
type PrototypeOutput = {
    id: string;
    name: string;
    description: string;
    system: string;
    running: boolean;
};
 
export const CreatePrototype: React.FC = () => {
    const [open, setOpen] = useAtom(createPrototypeAtom);
    const close = () => setOpen(false);
    const { systemId } = useParams();
    const [interfaces, isSuccessInterfaces] = useSystemInterfaces(systemId);
    const [diagrams, isSuccessDiagrams] = useSystemDiagrams(systemId);
    const [selectedInterfaces, setSelectedInterfaces] = useState([]);
    const [error, setError] = useState<string | null>(null);
    const [generationError, setGenerationError] = useState<string | null>(null);
    const [useAuthentication, setUseAuthentication] = useState(true);
    const [useSyntheticData, setUseSyntheticData] = useState(false); // New state for Synthetic Data
    const [syntheticCounts, setSyntheticCounts] = useState<Record<string, number>>({}); // state to store synthetic data counts
    const [showSyntheticModal, setShowSyntheticModal] = useState(false); // modal state
    const [syntheticInstructions, setSyntheticInstructions] = useState<string>(''); // state to store custom instructions for synthetic data generation
    const [databaseHash, setDatabaseHash] = useState<string | null>(null);
    const [databasePrototypes, setDatabasePrototypes] = useState([]);
    const [selectedDatabasePrototype, setSelectedDatabasePrototype] = useState(null);
    const [syntheticInstructionsPerNode, setSyntheticInstructionsPerNode] = useState<Record<string, string>>({});
 
 
    useEffect(() => {
        if (isSuccessInterfaces && interfaces) {
            setSelectedInterfaces(interfaces.map((e) => ({ label: e.name, value: e })));
        }
    }, [interfaces, isSuccessInterfaces]);
 
    useEffect(() => {
        const computeHash = async () => {
            if (systemId && isSuccessInterfaces) {
                const [classifiers, relations] = await Promise.all([
                    authAxios.get(`v1/metadata/systems/${systemId}/classes/`),
                    authAxios.get(`v1/metadata/systems/${systemId}/classifier-relations/`),
                ]);
 
                const interfaceNames = interfaces.map((e) => ({ name: e.name }));
                const inputString = `${systemId}${JSON.stringify(classifiers.data)}${JSON.stringify(relations.data)}${JSON.stringify(interfaceNames)}`;
                const hash = CryptoJS.SHA256(inputString).toString(CryptoJS.enc.Hex);
                setDatabaseHash(hash);
            }
        };
 
        computeHash();
    }, [systemId, interfaces, isSuccessInterfaces]);
 
    useEffect(() => {
        const fetchDatabasePrototypes = async () => {
            if (databaseHash) {
                try {
                    const { data } = await authAxios.get(`v1/generator/prototypes/${databaseHash}`);
                    setDatabasePrototypes(data.map((e) => ({ label: e.name, value: e })));
                } catch (error) {
                    console.error("Failed to fetch database prototypes:", error);
                }
            }
        };
 
        fetchDatabasePrototypes();
    }, [databaseHash]);
 
    const { mutateAsync, isPending } = useMutation<
        PrototypeOutput,
        unknown,
        PrototypeInput
    >({
        mutationFn: async (input) => {
            const { name, description, system, metadata } = input;
            if (selectedDatabasePrototype) {
                const { data } = await authAxios.post(`v1/generator/prototypes/?database_prototype_name=${selectedDatabasePrototype.label}`, {
                    name,
                    description,
                    system_id: system,
                    metadata,
                    database_hash: databaseHash,
                });
                return data
            }
            else {
                const { data } = await authAxios.post(`v1/generator/prototypes/?database_prototype_name=`, {
                    name,
                    description,
                    system_id: system,
                    metadata,
                    database_hash: databaseHash,
                });
                return data
            }
 
        },
        onError: (error) => {
            setGenerationError("An error occurred while creating the prototype!");
        },
    });
 
    const queryClient = useQueryClient();
    const onSubmit: React.FormEventHandler<HTMLFormElement> = async (e) => {
        e.preventDefault();
        setError(null);
 
        const formData = new FormData(e.currentTarget);
        const name = `${formData.get("name")}`.trim();
        const description = `${formData.get("description")}`;
        const running = Boolean(`${formData.get("running")}`);
        const metadata = {
            "diagrams": diagrams,
            "interfaces": selectedInterfaces,
            "useAuthentication": useAuthentication,
            "useSyntheticData": useSyntheticData,
            "syntheticCounts": syntheticCounts,
            "syntheticInstructions": syntheticInstructions,
            "syntheticInstructionsPerNode": syntheticInstructionsPerNode, // <-- new
        };
 
        const alphanumericRegex = /^[a-zA-Z0-9]+$/;
        if (!alphanumericRegex.test(name)) {
            setError("Name may only contain alphanumeric characters!");
            return;
        }
 
        if (!databaseHash) {
            setError("No database hash.");
            return;
        }
 
        mutateAsync({
            name,
            description,
            system: systemId || "",
            running,
            metadata,
            database_hash: databaseHash,
        }).then(() => {
            queryClient.invalidateQueries({ queryKey: ['prototypes', systemId] })
            close();
        }).catch((err) => {
            console.log(err)
        });
    };
 
    if (isPending) {
        return (
            <Modal open>
                <ModalDialog className="flex flex-row items-center gap-2">
                    <CircularProgress className="animate-spin" />
                    <Typography>
                        <h1 className="text-lg">Generating...</h1>
                    </Typography>
                </ModalDialog>
            </Modal>
        );
    }
 
    const hasName = (obj: any): obj is { name: string } => {
        return obj && typeof obj.name === 'string';
    };
 
    const extractNodeNames = (node: any) => {
        // Loop through all properties of the node (cls, enum, etc.)
        const subObjectWithName = Object.values(node).find((sub) => hasName(sub));
 
        return subObjectWithName ? subObjectWithName.name : null;
    };
 
 
    // Update synthetic data counts
    const updateValue = (name: string, value: number) => {
        setSyntheticCounts((prev) => ({
            ...prev,
            [name]: value, // Update the value for the specified name
        }));
    };
 
    const validClassNames = interfaces[0]?.data?.sections?.map((section) => section.class) || [];
 
    const getMultiplicityRules = (): {
        sourceName: string;
        targetName: string;
        rule: 'le' | 'ge' | 'eq';
    }[] => {
        if (!diagrams?.[0]?.edges || !diagrams?.[0]?.nodes) return [];
 
        const nodesById = Object.fromEntries(
            diagrams[0].nodes.map(node => [node.id, extractNodeNames(node)])
        );
 
        return diagrams[0].edges
            .filter(edge => edge.rel?.multiplicity)
            .map(edge => {
                const { multiplicity } = edge.rel;
                const sourceName = nodesById[edge.source_ptr];
                const targetName = nodesById[edge.target_ptr];
 
                if (!sourceName || !targetName) return null;
 
                const srcMult = multiplicity.source;
                const tgtMult = multiplicity.target;
 
                let rule: 'le' | 'ge' | 'eq' | null = null;
                if (srcMult === "1" && tgtMult === "1") rule = 'eq';
                else if (srcMult === "1" && tgtMult === "*") rule = 'le';
                else if (srcMult === "*" && tgtMult === "1") rule = 'ge';
 
                return rule ? { sourceName, targetName, rule } : null;
            })
            .filter(Boolean) as {
                sourceName: string;
                targetName: string;
                rule: 'le' | 'ge' | 'eq';
            }[];
    };
 
    const handleSyntheticValidation = () => {
        const rules = getMultiplicityRules();
        let isValid = true;
        let errorMessage = '';
 
        const hasValidNodes = diagrams[0]?.nodes?.some(node =>
            validClassNames.includes(node.cls_ptr)
        );
 
        if (!hasValidNodes) {
            setUseSyntheticData(false);
            setShowSyntheticModal(false);
            return;
        }
 
        rules.forEach(({ sourceName, targetName, rule }) => {
            const sourceCount = syntheticCounts[sourceName] ?? 0;
            const targetCount = syntheticCounts[targetName] ?? 0;
 
            if (rule === 'le') { // One to manny relation
                if (targetCount !== 0 && sourceCount === 0) {
                    errorMessage = `${sourceName} should have at least 1, due to one-to-many associoation with target ${targetName}`;
                    isValid = false;
                }
 
                else if (sourceCount > targetCount && targetCount !== 0) {
                    errorMessage = `${sourceName} must be less than or equal to ${targetName}`;
                    isValid = false;
                }
 
            } else if (rule === 'ge') { // many to one relation
                if (targetCount === 0 && sourceCount !== 0) {
                    errorMessage = `${targetName} should have at least 1, due to many-to-one associoation with source ${sourceName}`;
                    isValid = false;
                }
 
                else if (sourceCount < targetCount) {
                    errorMessage = `${sourceName} must be greater than or equal to ${targetName}`;
                    isValid = false;
                }
 
            } else if (rule === 'eq' && sourceCount !== targetCount) { // One to one relation
                isValid = false;
                errorMessage = `${sourceName} must have the same count as ${targetName}`;
            }
        });
 
        if (isValid) {
            setGenerationError(null);
            setShowSyntheticModal(false);
        } else {
            setGenerationError(errorMessage);
        }
    };
 
 
    return (
        <>
            <Modal open={open} onClose={() => { close(); setGenerationError(null) }}>
                <ModalDialog>
                    <div className="flex w-full flex-row justify-between pb-1">
                        <div className="flex flex-col">
                            <h1 className="font-bold">Generate Prototype</h1>
                            <h3 className="text-sm">Generate a new prototype using current metadata</h3>
                        </div>
                        <ModalClose
                            sx={{ position: "relative", top: 0, right: 0 }}
                        />
                    </div>
                    <Divider />
                    <form
                        id="create-project"
                        className="max-h-[400px] overflow-y-auto pr-2"
                        onSubmit={onSubmit}
                    >
                        <FormControl required>
                            <FormLabel>Name</FormLabel>
                            <Input name="name" placeholder="Prototype" required />
                            {error && (
                                <Typography sx={{ margin: '2px' }} className="text-sm text-red-400">
                                    {error}
                                </Typography>
                            )}
                        </FormControl>
                        <FormControl>
                            <FormLabel>Description</FormLabel>
                            <Input name="description" placeholder="A whole new world..." />
                        </FormControl>
                        <FormControl>
                            <FormLabel>Interfaces</FormLabel>
                            <Select
                                isMulti
                                name="interfaces"
                                options={interfaces.map((e) => ({ label: e.name, value: e }))}
                                value={selectedInterfaces}
                                onChange={(newValue) => setSelectedInterfaces(newValue ? newValue.map((v) => v.value) : [])}
                            />
                        </FormControl>
                        <FormControl>
                            <FormLabel>Reuse database</FormLabel>
                            <Select
                                name="database"
                                options={databasePrototypes}
                                value={selectedDatabasePrototype}
                                onChange={setSelectedDatabasePrototype}
                            />
                        </FormControl>
                        <FormControl>
                            <span className="flex flex-row items-center gap-2">
                                <Switch
                                    defaultChecked={useAuthentication}
                                    onChange={(e) => setUseAuthentication(e.target.checked)}
                                />
                                <FormLabel sx={{ marginTop: '4px' }}>Use Authentication</FormLabel>
                            </span>
                        </FormControl>
                        <FormControl>
                            <div className="flex flex-col gap-1">
                                <span className="flex flex-row items-center gap-2">
                                    <Switch
                                        checked={useSyntheticData}
                                        onChange={(e) => {
                                            const checked = e.target.checked;
                                            setUseSyntheticData(checked); // synthetic data generation button 
                                            if (checked) setShowSyntheticModal(true); // opens the new window for synthetic data
                                        }}
                                    />
                                    <FormLabel sx={{ marginTop: '4px' }}>Use Synthetic Data</FormLabel>
                                </span>
                            </div>
                        </FormControl>
                    </form>
                    <Divider />
                    <div className="flex flex-row pt-1">
                        <Button form="create-project" type="submit" disabled={isPending}>
                            {isPending ? (
                                <div className="flex flex-row gap-2">
                                    <CircularProgress className="animate-spin" />
                                    <p>Generating</p>
                                </div>
                            ) : "Create"}
                        </Button>
                    </div>
                    {generationError && (
                        <Typography sx={{ margin: '2px' }}>
                            <h1 className="text-lg text-red-800">{generationError}</h1>
                        </Typography>
                    )}
                </ModalDialog>
            </Modal>
 
            {/* Synthetic Data Popup Modal */}
            <Modal open={showSyntheticModal} onClose={() => setShowSyntheticModal(false)}>
                <ModalDialog>
                    <Typography level="h4">Specify Synthetic Data Amount Per Node</Typography>
                    {generationError && (
                        <Typography sx={{ margin: '2px' }}>
                            <h1 className="text-lg text-red-800">{generationError}</h1>
                        </Typography>
                    )}
                    {!interfaces[0]?.data?.sections || interfaces[0]?.data?.sections.length === 0 ? (
                        <Typography sx={{ marginTop: '4px', marginBottom: '8px' }}>
                            <span className="text-sm text-orange-600">
                                No section components found in pages. Please define at least one section component for this system in order to proceed with synthetic data generation.
                            </span>
                        </Typography>
                    ) : (
                        <>
                            {/*Custom instructions for synthetic data generation*/}
                            <FormControl className="mt-4">
                                <FormLabel>Custom Instructions</FormLabel>
                                <Input
                                    placeholder="e.g., 10 samples per user with real names"
                                    value={syntheticInstructions}
                                    onChange={(e) => setSyntheticInstructions(e.target.value)}
                                />
                            </FormControl>
 
                            <div className="max-h-[400px] overflow-y-auto pr-2 mt-2">
                                <div className="mb-6 border p-4 rounded shadow">
                                    {
                                        diagrams[0]?.nodes?.filter((node) => validClassNames.includes(node.cls_ptr))
                                            .map((node, index) => {
                                                const name = extractNodeNames(node);
                                                return (
                                                    <div key={index} className="mb-4">
                                                        <h4 className="font-semibold mb-2">Node {index + 1}: {name}</h4>
                                                        {name && (
                                                            <>
                                                                <input
                                                                    type="number"
                                                                    min="0"
                                                                    value={syntheticCounts[name] || 0}
                                                                    onChange={(e) => {
                                                                        const newValue = parseInt(e.target.value, 10);
                                                                        if (!isNaN(newValue) && newValue >= 0) {
                                                                            updateValue(name, newValue);
                                                                        }
                                                                    }}
                                                                    className="border border-gray-300 rounded px-2 py-1 w-32 mt-1"
                                                                    placeholder="Enter amount"
                                                                />
                                                                {/* Node-specific instruction input */}
                                                                <input
                                                                    type="text"
                                                                    value={syntheticInstructionsPerNode[name] || ""}
                                                                    onChange={(e) =>
                                                                        setSyntheticInstructionsPerNode((prev) => ({
                                                                            ...prev,
                                                                            [name]: e.target.value,
                                                                        }))
                                                                    }
                                                                    className="border border-gray-300 rounded px-2 py-1 w-full mt-2"
                                                                    placeholder={`Instruction for ${name} (optional)`}
                                                                />
                                                            </>
                                                        )}
                                                    </div>
 
                                                );
                                            })
                                    }
                                </div>
                            </div>
                        </>
                    )}
                    <Button onClick={handleSyntheticValidation}>Done</Button>
 
                </ModalDialog>
            </Modal>
 
 
        </>
    );
};
 
export default CreatePrototype;
